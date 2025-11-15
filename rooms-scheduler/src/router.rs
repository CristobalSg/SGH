use axum::{
    routing::post,
    Router,
};

use crate::controllers::rooms_scheduler::rooms_scheduler_controller;

pub fn create_router() -> Router {
    Router::new()
        .route("/api/v1/rooms/schedule", post(rooms_scheduler_controller))
}