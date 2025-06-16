############################
# Stage 1 – builder
############################
FROM debian:bookworm-slim AS builder

# Install git + CA certificates so HTTPS works
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Shallow clone 
RUN git clone --depth 1 https://github.com/jet-universe/particle_transformer.git

############################
# Stage 2 – distroless runtime
############################
FROM gcr.io/distroless/static:nonroot

WORKDIR /model_files

# Copy models from builder
COPY --from=builder /build/particle_transformer/models/ ./particle_transformer

# No default CMD, can override on docker run
