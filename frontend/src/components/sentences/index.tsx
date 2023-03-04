import React from "react";
import axios from "axios";
import { Link } from "react-router-dom";

function SentenceTop() {
  const [sentences, setSentences] = React.useState<SentenceType[]>([]);
  const [form, setForm] = React.useState<SentenceFormType>({
    sentence: "",
    translation: "",
  });

  React.useEffect(() => {
    axios
      .get("http://localhost:8888/sentences")
      .then(function (response) {
        return response.data;
      })
      .then(function (data) {
        console.log(data);
        setSentences(data);
      });
  }, []);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    e.preventDefault();
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  }

  function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    axios
      .post("http://localhost:8888/sentences", {
        sentence: form.sentence,
        translation: form.translation,
      })
      .then((resp) => {
        console.log(resp);
      });
  }

  return (
    <div className="flex p-2">
      <div className="flex-1 px-2">
        <h2 className="text-2xl">Sentence</h2>

        <ul className="px-2">
          {sentences.map((sentence) => (
            <li
              key={sentence.id}
              className="text-xl hover:bg-slate-400 px-2 rounded-md"
            >
              <Link to={`${sentence.id}`}>
                ({sentence.counter}) {sentence.sentence.substring(0, 50)}
              </Link>
            </li>
          ))}
        </ul>
      </div>

      <div className="flex-1">
        <div className="flex flex-col gap-2">
          <h2 className="text-2xl">Create Sentence</h2>

          <form
            action="http://localhost:8888/sentences"
            method="post"
            className="flex flex-col gap-2"
            onSubmit={(e) => handleSubmit(e)}
          >
            <input
              type="text"
              name="sentence"
              id="sentence"
              className="bg-slate-300 rounded-md pl-2"
              value={form.sentence}
              onChange={(e) => handleChange(e)}
            />
            <input
              type="text"
              name="translation"
              id="translation"
              className="bg-slate-300 rounded-md pl-2"
              value={form.translation}
              onChange={(e) => handleChange(e)}
            />
            <input
              type="submit"
              value="Create"
              className="bg-slate-800 text-slate-200 rounded-md"
            />
          </form>
        </div>
      </div>
    </div>
  );
}

export default SentenceTop;
