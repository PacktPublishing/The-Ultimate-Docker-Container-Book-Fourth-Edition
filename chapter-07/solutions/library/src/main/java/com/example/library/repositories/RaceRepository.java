package com.example.library.repositories;

import java.util.List;
import org.springframework.data.repository.CrudRepository;
import com.example.library.models.Race;

public interface RaceRepository extends CrudRepository<Race, Long> {
    List<Race> findBySpeciesId(Long speciesId);
}