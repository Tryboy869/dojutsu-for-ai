<?php
/**
 * Dojutsu-for-AI — PHP client
 * Prerequisites:
 *   git clone https://github.com/Tryboy869/dojutsu-for-ai
 *   cd dojutsu-for-ai && python allpath-runner.py daemon &
 *
 * Run: php client.php
 * PHP >= 8.1 required (unix socket support)
 */

function dojutsu(string $function, array $args = []): array
{
    $socketPath = '/tmp/allpath_runner.sock';
    $socket = socket_create(AF_UNIX, SOCK_STREAM, 0);
    if (!$socket) {
        throw new RuntimeException('socket_create failed: ' . socket_strerror(socket_last_error()));
    }

    if (!socket_connect($socket, $socketPath)) {
        throw new RuntimeException('Daemon not running? socket_connect: ' . socket_strerror(socket_last_error()));
    }

    $payload = json_encode([
        'package'  => 'dojutsu-agent',
        'function' => $function,
        'args'     => $args,
    ]);
    socket_send($socket, $payload, strlen($payload), 0);
    socket_shutdown($socket, 1); // stop writing

    $buffer = '';
    while (($chunk = socket_recv($socket, $data, 65536, 0)) !== false && $chunk > 0) {
        $buffer .= $data;
    }
    socket_close($socket);

    $result = json_decode($buffer, true);
    if (isset($result['error'])) {
        throw new RuntimeException('Dojutsu error: ' . $result['error']);
    }
    return $result;
}

// ── Usage ──────────────────────────────────────────────────────────────
$apiKey = getenv('GROQ_API_KEY') ?: throw new RuntimeException('Set GROQ_API_KEY env var');

// Full pipeline — Groq + Kimi
$result = dojutsu('run', [
    'Build a Laravel 11 REST API with Sanctum auth, Redis queue, and Horizon monitoring',
    $apiKey,
    'groq',
]);

echo "=== BYAKUGAN ===
" . $result['byakugan'] . "

";
echo "=== CODE ===
" . $result['execution'] . "
";
echo "
Time: " . round($result['total_time'], 1) . "s
";
echo "Skills: " . implode(', ', $result['skills_used'] ?? []) . "
";

// Structural analysis only (fast)
$analysis = dojutsu('byakugan', [
    'Add WebSocket broadcasting to an existing Laravel app',
    $apiKey,
    'groq',
]);
echo "
Structural vision:
" . $analysis['byakugan'] . "
";
