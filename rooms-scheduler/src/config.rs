
use std::sync::Arc;

pub struct Config {
    pub port: &'static str,
    pub jwt_secret: &'static str,
}

pub fn load_env() -> Arc<Config> {
    let port = std::env::var("ROOMS_SCHEDULER_PORT").unwrap_or_else(|_| "3000".to_string());
    let jwt_secret = std::env::var("JWT_SECRET").unwrap_or_else(|_| "default_secret".to_string());

    Arc::new(Config {
        port: Box::leak(port.into_boxed_str()),
        jwt_secret: Box::leak(jwt_secret.into_boxed_str()),
    })
}