FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 5105

ENV ASPNETCORE_URLS=http://+:5105

USER app
FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:9.0 AS build
ARG configuration=Release
WORKDIR /src
COPY ["csharp-sample.csproj", "./"]
RUN dotnet restore "csharp-sample.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "csharp-sample.csproj" -c $configuration -o /app/build

FROM build AS publish
ARG configuration=Release
RUN dotnet publish "csharp-sample.csproj" -c $configuration -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "csharp-sample.dll"]
