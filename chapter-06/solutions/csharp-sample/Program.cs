using OpenTelemetry.Resources;
using OpenTelemetry.Trace;
using System.Diagnostics;

var builder = WebApplication.CreateBuilder(args);

var activitySource = new ActivitySource("MyDotNetApp");
builder.Services.AddSingleton(activitySource);

builder.Services.AddOpenTelemetry()
    .ConfigureResource(resource => resource.AddService("csharp-sample"))
    .WithTracing(tracing => tracing
        .AddAspNetCoreInstrumentation()
        .AddHttpClientInstrumentation()
        .AddOtlpExporter(options =>
        {
            options.Endpoint = new Uri("http://localhost:4317");
        })
        .AddConsoleExporter());

builder.Services.AddOpenApi();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    app.Logger.LogInformation("Handling GET request for endpoint '/weatherforecast'");
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");

app.MapGet("/hello/{name}", (string name, ActivitySource activitySource) => {
    using var activity = activitySource.StartActivity("Hello");
    return Formatter.FormatString(name, activitySource);
});

app.MapGet("/warning", () => {
    app.Logger.LogWarning("Warning: accessing endpoint '/warning'");
    return "Just a warning";
});

app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}

class Formatter{
    public static string FormatString(string name, ActivitySource activitySource) {
        using var activity = activitySource.StartActivity("FormatString");
        activity?.SetTag("parameter.name", name);
        return $"Hello, ¶{name}";
    }
}