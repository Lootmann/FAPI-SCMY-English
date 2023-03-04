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

  // counter
  const [counter, setCounter] = React.useState<number>(0);

  React.useEffect(() => {
    setCounter(sentence.counter);
  }, []);

  function countSentence(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    sentenceId: number
  ) {
    e.preventDefault();

    axios
      .patch(`http://localhost:8888/sentences/${sentenceId}/count`)
      .then((resp) => {
        setCounter(resp.data.counter);
      });
  }

  return (
    <div className="flex justify-center">
      <div className="flex flex-col gap-2 w-2/3">
        <header className="flex flex-col bg-slate-400 rounded-md px-2 py-1">
          <div className="flex gap-4">
            <p>No.{sentence.id}</p>
            <p>
              <button
                onClick={(e) => countSentence(e, sentence.id)}
                className="bg-slate-200 rounded-md px-2"
              >
                conter: {counter}
              </button>
            </p>
          </div>
        </header>

        {/* TODO: Does textarea fit controlled components? */}
        {/* TODO: update textare how to method patch? */}

        {/* IMPL: handle form */}
        <form action="" method="post" className="flex gap-1">
          {/* IMPL: handleTextarea */}
          <textarea
            name="sentence"
            id="sentence"
            defaultValue={sentence.sentence}
            className="flex-1 bg-slate-300 rounded-md px-2 outline-none"
          ></textarea>

          {/* IMPL: handleTextarea */}
          <textarea
            name="translation"
            id="translation"
            defaultValue={sentence.translation}
            className="flex-1 bg-slate-300 rounded-md px-2 outline-none"
          ></textarea>
        </form>
      </div>
    </div>
  );
}

export default Sentence;
