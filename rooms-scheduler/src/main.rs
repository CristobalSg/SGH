mod config;
mod router;
mod controllers;
// mod models;

use crate::router::create_router;

#[tokio::main]
async fn main() {

    let config = config::load_env();

    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", config.port)).await.unwrap();
    
    let app = create_router();

    println!("Iniciando servicio asignador de salas ...");
    axum::serve(listener, app).await.unwrap();
}