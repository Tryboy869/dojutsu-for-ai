//! Dojutsu-for-AI — Rust client
//! Prerequisites:
//!   git clone https://github.com/Tryboy869/dojutsu-for-ai
//!   cd dojutsu-for-ai && python allpath-runner.py daemon &
//!
//! Cargo.toml deps:
//!   serde = { version = "1", features = ["derive"] }
//!   serde_json = "1"
//!   tokio = { version = "1", features = ["full"] }
use std::env;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::UnixStream;
use serde::{Deserialize, Serialize};

#[derive(Serialize)]
struct Request<'a> {
    package:  &'a str,
    function: &'a str,
    args:     Vec<&'a str>,
}

#[derive(Deserialize, Debug)]
struct DojutsuResult {
    byakugan:    Option<String>,
    mode_sage:   Option<String>,
    jougan:      Option<String>,
    execution:   Option<String>,
    skills_used: Option<Vec<String>>,
    total_time:  Option<f64>,
    error:       Option<String>,
}

async fn dojutsu(function: &str, args: Vec<&str>) -> anyhow::Result<DojutsuResult> {
    let mut stream = UnixStream::connect("/tmp/allpath_runner.sock").await?;

    let payload = serde_json::to_vec(&Request {
        package: "dojutsu-agent",
        function,
        args,
    })?;
    stream.write_all(&payload).await?;
    stream.shutdown().await?;

    let mut buf = Vec::new();
    stream.read_to_end(&mut buf).await?;

    let result: DojutsuResult = serde_json::from_slice(&buf)?;
    if let Some(err) = &result.error {
        anyhow::bail!("Dojutsu error: {}", err);
    }
    Ok(result)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let api_key = env::var("GROQ_API_KEY").expect("Set GROQ_API_KEY");

    // Full pipeline — Groq + Kimi
    let result = dojutsu("run", vec![
        "Build a Rust Axum REST API with JWT auth and PostgreSQL connection pool",
        &api_key,
        "groq",
    ]).await?;

    println!("=== BYAKUGAN ===");
    println!("{}", result.byakugan.unwrap_or_default());
    println!("\n=== CODE ===");
    println!("{}", result.execution.unwrap_or_default());
    println!("\nTime: {:.1}s", result.total_time.unwrap_or(0.0));
    println!("Skills: {:?}", result.skills_used.unwrap_or_default());

    Ok(())
}
