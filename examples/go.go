// Dojutsu-for-AI — Go client
// Prerequisites:
//   git clone https://github.com/Tryboy869/dojutsu-for-ai
//   cd dojutsu-for-ai && python allpath-runner.py daemon &
//
// Run: go run go.go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "net"
    "os"
    "time"
)

type DojutsuRequest struct {
    Package  string   `json:"package"`
    Function string   `json:"function"`
    Args     []string `json:"args"`
}

type DojutsuResult struct {
    Byakugan   string   `json:"byakugan"`
    ModeSage   string   `json:"mode_sage"`
    Jougan     string   `json:"jougan"`
    Execution  string   `json:"execution"`
    SkillsUsed []string `json:"skills_used"`
    TotalTime  float64  `json:"total_time"`
    Error      string   `json:"error,omitempty"`
}

func dojutsu(fn string, args []string) (*DojutsuResult, error) {
    conn, err := net.DialTimeout("unix", "/tmp/allpath_runner.sock", 5*time.Second)
    if err != nil {
        return nil, fmt.Errorf("daemon not running? %w", err)
    }
    defer conn.Close()
    conn.SetDeadline(time.Now().Add(120 * time.Second))

    req, _ := json.Marshal(DojutsuRequest{
        Package:  "dojutsu-agent",
        Function: fn,
        Args:     args,
    })
    conn.Write(req)

    data, err := io.ReadAll(conn)
    if err != nil {
        return nil, err
    }

    var result DojutsuResult
    if err := json.Unmarshal(data, &result); err != nil {
        return nil, fmt.Errorf("parse error: %w — raw: %s", err, string(data[:min(200, len(data))]))
    }
    if result.Error != "" {
        return nil, fmt.Errorf("dojutsu error: %s", result.Error)
    }
    return &result, nil
}

func min(a, b int) int {
    if a < b {
        return a
    }
    return b
}

func main() {
    apiKey := os.Getenv("GROQ_API_KEY")
    if apiKey == "" {
        fmt.Fprintln(os.Stderr, "Set GROQ_API_KEY env var")
        os.Exit(1)
    }

    // Full pipeline
    result, err := dojutsu("run", []string{
        "Build a Go HTTP middleware for JWT authentication with refresh token rotation",
        apiKey,
        "groq",
    })
    if err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        os.Exit(1)
    }

    fmt.Println("=== BYAKUGAN ===")
    fmt.Println(result.Byakugan)
    fmt.Println("\n=== CODE ===")
    fmt.Println(result.Execution)
    fmt.Printf("\nTime: %.1fs | Skills: %v\n", result.TotalTime, result.SkillsUsed)
}
