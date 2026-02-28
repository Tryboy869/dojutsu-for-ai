// Dojutsu-for-AI — C# (.NET 8) client
// Prerequisites:
//   git clone https://github.com/Tryboy869/dojutsu-for-ai
//   cd dojutsu-for-ai && python allpath-runner.py daemon &
//
// Run: dotnet run (add <Nullable>enable</Nullable> in .csproj)
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

record DojutsuRequest(
    [property: JsonPropertyName("package")]  string Package,
    [property: JsonPropertyName("function")] string Function,
    [property: JsonPropertyName("args")]     string[] Args
);

record DojutsuResult(
    [property: JsonPropertyName("byakugan")]    string?   Byakugan,
    [property: JsonPropertyName("mode_sage")]   string?   ModeSage,
    [property: JsonPropertyName("jougan")]      string?   Jougan,
    [property: JsonPropertyName("execution")]   string?   Execution,
    [property: JsonPropertyName("skills_used")] string[]? SkillsUsed,
    [property: JsonPropertyName("total_time")]  double?   TotalTime,
    [property: JsonPropertyName("error")]       string?   Error
);

static class Dojutsu
{
    const string SocketPath = "/tmp/allpath_runner.sock";

    public static async Task<DojutsuResult> CallAsync(string function, params string[] args)
    {
        using var socket = new Socket(AddressFamily.Unix, SocketType.Stream, ProtocolType.Unspecified);
        await socket.ConnectAsync(new UnixDomainSocketEndPoint(SocketPath));

        var payload = JsonSerializer.SerializeToUtf8Bytes(new DojutsuRequest("dojutsu-agent", function, args));
        await socket.SendAsync(payload);
        socket.Shutdown(SocketShutdown.Send);

        var buffer = new List<byte>();
        var chunk  = new byte[65536];
        int received;
        while ((received = await socket.ReceiveAsync(chunk)) > 0)
            buffer.AddRange(chunk[..received]);

        var result = JsonSerializer.Deserialize<DojutsuResult>(buffer.ToArray())
            ?? throw new Exception("Empty response");

        if (result.Error is not null)
            throw new Exception($"Dojutsu error: {result.Error}");

        return result;
    }
}

// ── Usage ──────────────────────────────────────────────────────────────
var apiKey = Environment.GetEnvironmentVariable("GROQ_API_KEY")
    ?? throw new Exception("Set GROQ_API_KEY env var");

// Full pipeline — Groq + Kimi
var result = await Dojutsu.CallAsync(
    "run",
    "Build an ASP.NET Core 8 Web API with JWT auth, EF Core, Redis distributed cache, and Hangfire background jobs",
    apiKey,
    "groq"
);

Console.WriteLine("=== BYAKUGAN ===");
Console.WriteLine(result.Byakugan);
Console.WriteLine("\n=== CODE ===");
Console.WriteLine(result.Execution);
Console.WriteLine($"\nTime: {result.TotalTime:F1}s");
Console.WriteLine($"Skills: {string.Join(", ", result.SkillsUsed ?? [])}");
