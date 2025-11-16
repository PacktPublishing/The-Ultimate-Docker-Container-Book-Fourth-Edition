FROM mcr.microsoft.com/dotnet/sdk:9.0
WORKDIR /app
COPY *.csproj .
RUN dotnet restore
COPY . .
CMD ["dotnet", "test", "--logger:console;verbosity=detailed"]