FROM gradle:8.10.2-jdk21
WORKDIR /app
COPY build.gradle.kts ./
COPY settings.gradle.kts ./ 
COPY gradle ./gradle
RUN gradle build --no-daemon --quiet || true
COPY src ./src
RUN gradle bootJar --no-daemon
EXPOSE 8080
CMD ["java", "-jar", "build/libs/library-0.0.1-SNAPSHOT.jar"]
