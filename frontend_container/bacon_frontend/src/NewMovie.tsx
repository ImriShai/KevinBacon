import React, { useState, type ChangeEvent, type FormEvent } from "react";

type Actor = {
  id: string;
  name: string;
};

type Movie = {
  id: string;
  name: string;
};

type Payload = {
  Movie: Movie;
  Actors: Actor[];
};

const NewMovie: React.FC = () => {
  const [movieId, setMovieId] = useState<string>("");
  const [movieName, setMovieName] = useState<string>("");
  const [actors, setActors] = useState<Actor[]>(([
    { id: "", name: "" }
  ]));

  const handleActorChange = (
    index: number,
    field: keyof Actor,
    value: string
  ) => {
    const updatedActors = [...actors];
    updatedActors[index][field] = value;
    setActors(updatedActors);
  };

  const addActor = () => {
    setActors([...actors, { id: "", name: "" }]);
  };

  const removeActor = (index: number) => {
    setActors(actors.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const movie: Movie = {
      id: movieId,
      name: movieName
    };

    const payload: Payload = {
      Movie: movie,
      Actors: actors
    };

    try {
      const response = await fetch("/api/new-movie", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error("Failed to submit");

      const data = await response.text();
      console.log("Success:", data);

      // Reset form
      setMovieId("");
      setMovieName("");
      setActors([{ id: "", name: "" }]);

    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Add New Movie</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Movie ID:</label>
          <input
            type="text"
            value={movieId}
            onChange={(e: ChangeEvent<HTMLInputElement>) =>
              setMovieId(e.target.value)
            }
            required
          />
        </div>

        <div>
          <label>Movie Name:</label>
          <input
            type="text"
            value={movieName}
            onChange={(e: ChangeEvent<HTMLInputElement>) =>
              setMovieName(e.target.value)
            }
            required
          />
        </div>

        <h3>Actors</h3>

        {actors.map((actor, index) => (
          <div key={index} style={{ marginBottom: "10px" }}>
            <input
              type="text"
              placeholder="Actor ID"
              value={actor.id}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                handleActorChange(index, "id", e.target.value)
              }
              required
            />

            <input
              type="text"
              placeholder="Actor Name"
              value={actor.name}
              onChange={(e: ChangeEvent<HTMLInputElement>) =>
                handleActorChange(index, "name", e.target.value)
              }
              required
            />

            <button
              type="button"
              onClick={() => removeActor(index)}
              disabled={actors.length === 1}
            >
              Remove
            </button>
          </div>
        ))}

        <button type="button" onClick={addActor}>
          + Add Actor
        </button>

        <br /><br />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default NewMovie;