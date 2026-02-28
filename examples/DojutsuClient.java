/**
 * Dojutsu-for-AI — Java client
 * Prerequisites:
 *   git clone https://github.com/Tryboy869/dojutsu-for-ai
 *   cd dojutsu-for-ai && python allpath-runner.py daemon &
 *
 * Compile: javac -cp json-20240303.jar DojutsuClient.java
 * Run:     java -cp .:json-20240303.jar DojutsuClient
 * Dep:     https://mvnrepository.com/artifact/org.json/json
 */
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.*;
import java.net.StandardProtocolFamily;
import java.net.UnixDomainSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;

public class DojutsuClient {

    private static final String SOCKET_PATH = "/tmp/allpath_runner.sock";
    private static final int TIMEOUT_MS     = 120_000;

    public static JSONObject call(String function, String... args) throws IOException {
        var address = UnixDomainSocketAddress.of(Path.of(SOCKET_PATH));
        try (var channel = SocketChannel.open(StandardProtocolFamily.UNIX)) {
            channel.connect(address);

            var payload = new JSONObject();
            payload.put("package",  "dojutsu-agent");
            payload.put("function", function);
            var argsArr = new JSONArray();
            for (var a : args) argsArr.put(a);
            payload.put("args", argsArr);

            var bytes = payload.toString().getBytes(StandardCharsets.UTF_8);
            channel.write(ByteBuffer.wrap(bytes));
            channel.shutdownOutput();

            var out = new ByteArrayOutputStream();
            var buf = ByteBuffer.allocate(65536);
            while (channel.read(buf) > 0) {
                out.write(buf.array(), 0, buf.position());
                buf.clear();
            }
            var result = new JSONObject(out.toString(StandardCharsets.UTF_8));
            if (result.has("error")) {
                throw new RuntimeException("Dojutsu error: " + result.getString("error"));
            }
            return result;
        }
    }

    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("GROQ_API_KEY");
        if (apiKey == null || apiKey.isBlank()) {
            System.err.println("Set GROQ_API_KEY env var");
            System.exit(1);
        }

        // Full pipeline — Groq + Kimi
        var result = call(
            "run",
            "Build a Spring Boot REST API with JWT auth, Redis caching, and Flyway migrations",
            apiKey,
            "groq"
        );

        System.out.println("=== BYAKUGAN ===");
        System.out.println(result.getString("byakugan"));
        System.out.println("\n=== CODE ===");
        System.out.println(result.getString("execution"));
        System.out.printf("\nTime: %.1fs%n", result.getDouble("total_time"));

        // Quick skill count
        var info = call("skills_count");
        System.out.println("Skills indexed: " + info.getJSONObject("count"));
    }
}
