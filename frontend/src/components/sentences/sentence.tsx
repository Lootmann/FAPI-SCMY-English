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
  // show translation
  const [show, setShow] = React.useState<boolean>(false);

  // textarea form
  const [textarea, setTextarea] = React.useState<SentenceFormType>({
    sentence: "",
    translation: "",
  });

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    axios
      .patch(`http://localhost:8888/sentences/${sentence.id}`, {
        sentence: textarea.sentence,
        translation: textarea.translation,
      })
      .then((resp) => {
        console.log(resp.data);
      });
  }

  function handleChange(e: React.ChangeEvent<HTMLTextAreaElement>) {
    e.preventDefault();
    const { name, value } = e.target;
    setTextarea({ ...textarea, [name]: value });
  }

  function countSentence(
    e: React.MouseEvent<HTMLButtonElement, MouseEvent>,
    sentenceId: number
  ) {
    e.preventDefault();

    // TODO: patch? Incrementing counter should be sent by POST method, right?
    axios
      .patch(`http://localhost:8888/sentences/${sentenceId}/count`)
      .then((resp) => {
        setCounter(resp.data.counter);
      });
  }

  // init counter, textarea
  React.useEffect(() => {
    setCounter(sentence.counter);

    textarea.sentence = sentence.sentence;
    textarea.translation = sentence.translation;
    setTextarea(textarea);
  }, []);

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

            <p>
              <button
                onClick={() => setShow(!show)}
                className="bg-slate-200 rounded-md px-2"
              >
                {show == true ? (
                  <span>hide translation</span>
                ) : (
                  <span>show translation</span>
                )}
              </button>
            </p>

            {/* FIXME: HOW can I use the Post Form Like this?! */}
            <form
              method="post"
              className="bg-slate-200 rounded-md px-2 hover:bg-yellow-500 transition-all duration-200"
              onSubmit={(e) => handleSubmit(e)}
            >
              <input type="submit" value="Update" />
            </form>
          </div>
        </header>

        <form
          method="post"
          className="flex gap-1"
          onSubmit={(e) => e.preventDefault()}
        >
          <textarea
            name="sentence"
            id="sentence"
            value={textarea?.sentence}
            className="flex-1 bg-slate-300 rounded-md px-2 outline-none"
            onChange={(e) => handleChange(e)}
          ></textarea>

          {show && (
            <textarea
              name="translation"
              id="translation"
              value={textarea?.translation}
              className="flex-1 bg-slate-300 rounded-md px-2 outline-none"
              onChange={(e) => handleChange(e)}
            ></textarea>
          )}
        </form>
      </div>
    </div>
  );
}

export default Sentence;
