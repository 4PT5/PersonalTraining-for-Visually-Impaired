import React, { useState } from 'react';
import { useSpeechRecognition } from 'react-speech-kit';

const SttFunction = () => {
  const [lang, setLang] = useState('ko-KR');
  const [value, setValue] = useState('');
  const [blocked, setBlocked] = useState(false);

  const onEnd = () => {
    // You could do something here after listening has finished
  };

  const onResult = (result) => {
    setValue(result);
  };

  const onError = (event) => {
    if (event.error === 'not-allowed') {
      setBlocked(true);
    }
  };

  const { listen, listening, stop, supported } = useSpeechRecognition({
    onResult,
    onEnd,
    onError,
  });

  const toggle = listening
    ? stop
    : () => {
      setBlocked(false);
      listen({ lang });
    };

  return (
    <form id="speech-recognition-form">
      {!supported && (
        <p>
          Oh no, it looks like your browser doesn't support Speech Recognition.
        </p>
      )}
      {supported && (
        <React.Fragment>
          <label htmlFor="transcript"></label>
          <textarea
            id="transcript"
            name="transcript"
            placeholder=""
            value={value}
            rows={3}
          />
          <button disabled={blocked} type="button" onClick={toggle}>
            {listening ? 'Stop' : 'Listen'}
          </button>
          {blocked && (
            <p style={{ color: 'red' }}>
              The microphone is blocked for this site in your browser.
            </p>
          )}
        </React.Fragment>
      )}
    </form>
  );
};

export default SttFunction;