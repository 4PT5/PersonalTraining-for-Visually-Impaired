import React, { useState } from 'react'
import { useSpeechSynthesis } from 'react-speech-kit';

function TtsFunction(props) {
    const [value, setValue] = useState('');
    const { speak } = useSpeechSynthesis();

    return (
        <div>
            <textarea
                value={value}
                onChange={(event) => setValue(event.target.value)}
                rows={3}
            />
            <button onClick={() => speak({ text: value })}>Speak</button>
        </div>
    );
}

export default TtsFunction;