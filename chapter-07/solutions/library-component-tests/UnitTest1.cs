using System.Text.Json;

namespace library_component_tests;

public record Species(int id, string name, string description);

public class UnitTest1
{
    [Fact]
    public async Task can_add_species()
    {
        // Arrange
        var client = new HttpClient();
        client.BaseAddress = new Uri("http://localhost:8080/species");
        var species = new Species(1, "Lion", "Big cat");
        var json = JsonSerializer.Serialize(species);
        var body = new StringContent(json, System.Text.Encoding.UTF8, "application/json");

        // Act
        var response = await client.PostAsync("", body);

        // Assert
        Assert.Equal(System.Net.HttpStatusCode.OK, response.StatusCode);
        var responseBody = await response.Content.ReadAsStringAsync();
        var addedSpecies = JsonSerializer.Deserialize<Species>(responseBody);
        Assert.NotNull(addedSpecies);
        Assert.Equal(species.id, addedSpecies.id);
        Assert.Equal(species.name, addedSpecies.name);
        Assert.Equal(species.description, addedSpecies.description);
    }

    [Fact]
    public async Task can_get_species_by_id()
    {
        // Arrange
        var client = new HttpClient();
        var species = new Species(1, "Tiger", "Elegant cat");
        var json = JsonSerializer.Serialize(species);
        var body = new StringContent(json, System.Text.Encoding.UTF8, "application/json");
        var res = await client.PostAsync("http://localhost:8080/species", body);

        // Act
        var response = await client.GetAsync("http://localhost:8080/species/1");

        // Assert
        Assert.Equal(System.Net.HttpStatusCode.OK, response.StatusCode);
        var responseBody = await response.Content.ReadAsStringAsync();
        var addedSpecies = JsonSerializer.Deserialize<Species>(responseBody);
        Assert.NotNull(addedSpecies);
        Assert.Equal(species.id, addedSpecies.id);
        Assert.Equal(species.name, addedSpecies.name);
        Assert.Equal(species.description, addedSpecies.description);
    }
}
