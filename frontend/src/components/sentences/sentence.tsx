import React from "react";
import axios from "axios";
import { useLoaderData } from "react-router-dom";

export async function loader({ params }: SentenceProp) {
  const sentence = await axios
    .get(`http://localhost:8888/sentences/${params.sentenceId}`)
    .then((resp) => {
      return resp.data;
    });

  return sentence;
}

export function Sentence() {
  const sentence = useLoaderData() as SentenceType;

  return (
    <div>
      <h2>Sentence</h2>
      <p>No.{sentence.id}</p>
      <p>{sentence.sentence}</p>
      <p>{sentence.translation}</p>
    </div>
  );
}

export default Sentence;
