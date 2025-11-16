# Stage 1: build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Create project
RUN dotnet new web -n cs-service
WORKDIR /src/cs-service

# Add prometheus package
RUN dotnet add package prometheus-net.AspNetCore

# Copy Program.cs from your local folder into project
COPY Program.cs .

# Publish the app
RUN dotnet publish -c Release -o /out

# Stage 2: runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /out .
EXPOSE 8083
ENTRYPOINT ["dotnet", "cs-service.dll"]