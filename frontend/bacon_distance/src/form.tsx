import { useState, type ChangeEvent, type FormEvent } from "react";

const DISTANCE_API: string = "http://172.26.247.4:5555/calculate";

export default function DistanceForm() {
  const [actorName, setActorName] = useState<string>("");

  function handleChange(e: ChangeEvent<HTMLInputElement>): void {
    setActorName(e.target.value);
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>): Promise<void> {
    e.preventDefault();

    const postData = {
      name: actorName,
    };

    try {
      const response = await fetch(DISTANCE_API, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          
        },
        body: JSON.stringify(postData),
      });

      const data = await response.text();
      alert(data);
    } catch (error) {
      console.error(error);
      alert("Request failed");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Enter the actor name to calculate bacon distance:
        <input
          type="text"
          value={actorName}
          onChange={handleChange}
        />
      </label>
      <input type="submit" />
    </form>
  );
}