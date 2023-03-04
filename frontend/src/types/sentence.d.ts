type SentenceType = {
  id: number;
  counter: number;
  sentence: string;
  translation: string;
};

type SentenceFormType = {
  sentence: string;
  translation: string;
};

type SentenceProp = {
  params: {
    sentenceId: number;
  };
};
