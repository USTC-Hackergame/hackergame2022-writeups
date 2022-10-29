import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.GeneralSecurityException;
import java.security.MessageDigest;
import java.security.PublicKey;
import java.security.SecureRandom;
import java.security.Signature;
import java.security.cert.CertificateFactory;
import java.util.Base64;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.OptionalDouble;
import java.util.Random;
import java.util.Stack;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ForkJoinPool;
import java.util.regex.Pattern;

import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLOutputFactory;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

public final class GuessNumber {
   private static final Path CERT;
   private static final Path INDEX;
   private static final Path STYLE;
   private static final Path SOURCE_FILE;

   private static final Map<Token, State> STATES;
   private static final XMLInputFactory XML_INPUTS;
   private static final XMLOutputFactory XML_OUTPUTS;

   private static final String PORT = "GUESS_NUMBER_PORT";
   private static final String FLAG_PREFIX = "GUESS_NUMBER_FLAG_PREFIX";
   private static final String FLAG_SECRET = "GUESS_NUMBER_FLAG_SECRET";
   private static final String CERT_FILE_PATH = "GUESS_NUMBER_CERT_FILE_PATH";
   private static final String INDEX_FILE_PATH = "GUESS_NUMBER_INDEX_FILE_PATH";
   private static final String STYLE_FILE_PATH = "GUESS_NUMBER_STYLE_FILE_PATH";
   private static final String SOURCE_FILE_PATH = "GUESS_NUMBER_SOURCE_FILE_PATH";

   static {
      STATES = new ConcurrentHashMap<>();
      XML_INPUTS = XMLInputFactory.newFactory();
      XML_OUTPUTS = XMLOutputFactory.newFactory();
      CERT = Path.of(System.getenv().getOrDefault(CERT_FILE_PATH, "cert.pem"));
      INDEX = Path.of(System.getenv().getOrDefault(INDEX_FILE_PATH, "index.html"));
      STYLE = Path.of(System.getenv().getOrDefault(STYLE_FILE_PATH, "github-markdown.css"));
      SOURCE_FILE = Path.of(System.getenv().getOrDefault(SOURCE_FILE_PATH, "GuessNumber.java"));
   }

   private record Token(String user, String raw) {
      private static final Pattern AUTHORIZATION_PATTERN;
      private static final MessageDigest SHA256_DIGEST;
      private static final Optional<PublicKey> KEY;

      static {
         try {
            AUTHORIZATION_PATTERN = Pattern.compile("[Bb]earer\\s+(0|[1-9]\\d*):([A-Za-z\\d+/]+=*)");
            SHA256_DIGEST = MessageDigest.getInstance("SHA-256");
            KEY = readPublicKeyFromPem(CERT);
         } catch (GeneralSecurityException e) {
            throw new RuntimeException(e);
         }
      }

      private static Optional<PublicKey> readPublicKeyFromPem(Path path) throws GeneralSecurityException {
         var factory = CertificateFactory.getInstance("X.509");
         try (var inputStream = Files.newInputStream(path)) {
            return Optional.of(factory.generateCertificate(inputStream).getPublicKey());
         } catch (IOException e) {
            return Optional.empty();
         }
      }

      private static Token from(com.sun.net.httpserver.HttpExchange exchange) throws GeneralSecurityException {
         var authorization = exchange.getRequestHeaders().getFirst("Authorization");
         try {
            var matcher = Token.AUTHORIZATION_PATTERN.matcher(Objects.requireNonNullElse(authorization, ""));
            if (matcher.matches()) {
               // unpack user and signature
               var userStr = matcher.group(1);
               var signatureStr = matcher.group(2);
               var tokenStr = userStr + ':' + signatureStr;
               if (KEY.isEmpty()) return new Token(userStr, tokenStr);
               // prepare signature
               var signature = Signature.getInstance("SHA256withECDSA");
               var signatureBytes = Base64.getDecoder().decode(signatureStr);
               // verify signature
               signature.initVerify(KEY.get());
               signature.update(userStr.getBytes(StandardCharsets.UTF_8));
               if (signature.verify(signatureBytes)) return new Token(userStr, tokenStr);
            }
         } catch (IllegalArgumentException ignored) {
            // fall through
         }
         throw new GeneralSecurityException();
      }

      public String flag() {
         var prefix = System.getenv(FLAG_PREFIX);
         var input = System.getenv(FLAG_SECRET) + ":" + this.raw;
         var digest = SHA256_DIGEST.digest(input.getBytes(StandardCharsets.UTF_8));
         return String.format("flag{%s-%016x}", prefix, ByteBuffer.wrap(digest).getLong());
      }
   }

   private record State(Token token, int passed, int talented, double number, OptionalDouble previous) {
      private static final Random RNG = new SecureRandom();

      private State(Token token) {
         this(token, 0, 0, RNG.nextInt(1, 1000000) * 1e-6, OptionalDouble.empty());
      }

      private void collect(XMLStreamWriter writer) throws XMLStreamException {
         writer.writeStartDocument();
         // <state>
         writer.writeStartElement("state");
         // <name>
         writer.writeStartElement("name");
         writer.writeCharacters(this.token.user());
         writer.writeEndElement();
         // </name><passed>
         writer.writeStartElement("passed");
         writer.writeCharacters(Integer.toString(this.passed));
         writer.writeEndElement();
         // </passed><talented>
         writer.writeStartElement("talented");
         writer.writeCharacters(Integer.toString(this.talented));
         writer.writeEndElement();
         // </talented>
         if (this.previous.isPresent()) {
            // <guess>
            var previous = this.previous.getAsDouble();

            var isLess = previous < this.number - 1e-6 / 2;
            var isMore = previous > this.number + 1e-6 / 2;

            writer.writeStartElement("guess");
            writer.writeAttribute("less", Boolean.toString(isLess));
            writer.writeAttribute("more", Boolean.toString(isMore));
            writer.writeCharacters(Double.toString(previous));
            writer.writeEndElement();
            // </guess>
         }
         if (this.talented > 0) {
            // <flag>
            writer.writeStartElement("flag");
            writer.writeCharacters(this.token.flag());
            writer.writeEndElement();
            // </flag>
         }
         writer.writeEndElement();
         // </state>
      }

      private State update(XMLEventReader reader) throws XMLStreamException {
         var result = Optional.<State>empty();
         var nameStack = new Stack<String>();
         while (reader.hasNext()) {
            var event = reader.nextEvent();
            if (event.isStartElement()) {
               var name = event.asStartElement().getName().getLocalPart();
               nameStack.push(name);
            }
            if (event.isEndElement()) {
               if (nameStack.empty()) throw new XMLStreamException();
               var name = event.asEndElement().getName().getLocalPart();
               if (!name.equals(nameStack.pop())) throw new XMLStreamException();
            }
            if (event.isCharacters()) {
               var path = List.of("state", "guess");
               if (!path.equals(nameStack)) continue;
               if (result.isPresent()) throw new XMLStreamException();
               try {
                  var guess = Double.parseDouble(event.asCharacters().getData());

                  var isLess = guess < this.number - 1e-6 / 2;
                  var isMore = guess > this.number + 1e-6 / 2;

                  var isPassed = !isLess && !isMore;
                  var isTalented = isPassed && this.previous.isEmpty();

                  var newPassed = isPassed ? this.passed + 1 : this.passed;
                  var newTalented = isTalented ? this.talented + 1 : this.talented;
                  var newNumber = isPassed ? RNG.nextInt(1, 1000000) * 1e-6 : this.number;
                  var newPrevious = isPassed ? OptionalDouble.empty() : OptionalDouble.of(guess);

                  result = Optional.of(new State(this.token, newPassed, newTalented, newNumber, newPrevious));
               } catch (NumberFormatException e) {
                  throw new XMLStreamException(e);
               }
            }
         }
         if (!nameStack.empty()) throw new XMLStreamException();
         if (result.isEmpty()) throw new XMLStreamException();
         return result.get();
      }
   }

   private static void dispatch(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      var method = exchange.getRequestMethod().toUpperCase(Locale.ROOT);
      switch (method + ' ' + exchange.getRequestURI().getPath()) {
         case "HEAD /", "HEAD /index.html", "HEAD /github-markdown.css" -> head(exchange);
         case "HEAD /GuessNumber.java", "HEAD /state" -> head(exchange);
         case "GET /", "GET /index.html" -> index(exchange);
         case "GET /github-markdown.css" -> style(exchange);
         case "GET /GuessNumber.java" -> source(exchange);
         case "POST /state" -> update(exchange);
         case "GET /state" -> collect(exchange);
         default -> bad(exchange);
      }
   }

   private static void head(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      exchange.sendResponseHeaders(200, -1);
      exchange.close();
   }

   private static void index(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      try (var stream = Files.newInputStream(INDEX)) {
         exchange.getResponseHeaders().set("Content-Type", "text/html;charset=utf-8");
         exchange.sendResponseHeaders(200, Files.size(INDEX));
         stream.transferTo(exchange.getResponseBody());
         exchange.getResponseBody().flush();
         exchange.close();
      }
   }

   private static void style(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      try (var stream = Files.newInputStream(STYLE)) {
         exchange.getResponseHeaders().set("Content-Type", "text/css;charset=utf-8");
         exchange.sendResponseHeaders(200, Files.size(STYLE));
         stream.transferTo(exchange.getResponseBody());
         exchange.getResponseBody().flush();
         exchange.close();
      }
   }

   private static void source(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      try (var stream = Files.newInputStream(SOURCE_FILE)) {
         exchange.getResponseHeaders().set("Content-Type", "text/plain;charset=utf-8");
         exchange.sendResponseHeaders(200, Files.size(SOURCE_FILE));
         stream.transferTo(exchange.getResponseBody());
         exchange.getResponseBody().flush();
         exchange.close();
      }
   }

   private static void collect(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      try {
         var token = Token.from(exchange);
         var stream = new ByteArrayOutputStream();
         var state = STATES.computeIfAbsent(token, State::new);

         state.collect(XML_OUTPUTS.createXMLStreamWriter(stream, "UTF-8"));

         exchange.getResponseHeaders().set("Content-Type", "text/xml;charset=utf-8");
         exchange.sendResponseHeaders(200, stream.size());
         stream.writeTo(exchange.getResponseBody());
         exchange.getResponseBody().flush();
         exchange.close();
      } catch (GeneralSecurityException ignored) {
         unauthorized(exchange);
      } catch (XMLStreamException ignored) {
         bad(exchange);
      }
   }

   private static void update(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      try {
         var input = exchange.getRequestBody().readAllBytes();
         var token = Token.from(exchange);
         var replaced = false;
         while (!replaced) {
            var stream = new ByteArrayInputStream(input);
            var oldState = STATES.computeIfAbsent(token, State::new);
            var newState = oldState.update(XML_INPUTS.createXMLEventReader(stream, "UTF-8"));

            replaced = STATES.replace(token, oldState, newState);
         }
         exchange.sendResponseHeaders(204, -1);
         exchange.close();
      } catch (GeneralSecurityException ignored) {
         unauthorized(exchange);
      } catch (XMLStreamException ignored) {
         bad(exchange);
      }
   }

   private static void unauthorized(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      exchange.sendResponseHeaders(401, 0);
      exchange.close();
   }

   private static void bad(com.sun.net.httpserver.HttpExchange exchange) throws IOException {
      exchange.sendResponseHeaders(400, 0);
      exchange.close();
   }

   public static void main(String[] args) throws Exception {
      var address = new InetSocketAddress(Integer.parseInt(System.getenv().getOrDefault(PORT, "8080")));
      var server = com.sun.net.httpserver.HttpServer.create(address, /* backlog */0);
      server.createContext("/", GuessNumber::dispatch);
      server.setExecutor(ForkJoinPool.commonPool());
      server.start();

      System.out.println("The guess number server started at " + address + ".");
   }
}
