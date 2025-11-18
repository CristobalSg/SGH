use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Room {
    pub name: String,
    pub capacity: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Activity {
    pub id: u32,
    pub subject: String,
    pub room: Room,
    pub time_slots: Vec<u32>,
    pub students_count: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ActivitiesRequest {
    pub activities: Vec<Activity>,
    pub rooms: Vec<Room>,
}