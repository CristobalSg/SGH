FROM rust:1.91-alpine3.22 as builder

WORKDIR /app

COPY Cargo.toml Cargo.lock .

RUN mkdir src

COPY src ./src

RUN cargo build --release

FROM alpine:3.22

CMD ["/app/target/release/rooms-scheduler"]