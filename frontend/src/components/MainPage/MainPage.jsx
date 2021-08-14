import React, { useState, useCallback, CSSProperties, useEffect } from 'react'
import { useTransition, animated, AnimatedProps, useSpringRef } from '@react-spring/web'
import styles from './MainPage.module.css';
import start_script from './Sections/script.js';
import Sttfunction from './Sections/SttFunction';
import Ttsfunction from './Sections/TtsFunction';

const page = [
    ({ style }) => (
        <animated.div style={{ ...style, background: "black" }}>{start_script[0].text}</animated.div>
    ),
    ({ style }) => (
        <animated.div style={{ ...style, background: "black" }}>{start_script[1].text}</animated.div>
    ),
    ({ style }) => (
        <animated.div style={{ ...style, background: "black" }}>{start_script[2].text}</animated.div>
    ),
    ({ style }) => (
        <animated.div style={{ ...style, background: "black" }}>{start_script[3].text}</animated.div>
    ),
];

function MainPage() {

    const [index, setIndex] = useState(0);
    const [script, setScript] = useState([]);
    const [pages, setPages] = useState(page);
    const [pageLength, setPageLength] = useState(4);

    const onClick = useCallback(() => setIndex(state => (state + 1) % pageLength), [])

    const transRef = useSpringRef()
    const transitions = useTransition(index, {
        ref: transRef,
        keys: null,
        from: { opacity: 0, transform: 'translate3d(100%,0,0)' },
        enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
        leave: { opacity: 0, transform: 'translate3d(-50%,0,0)' },
    })

    const getText = (text) => {
        let input_ =
            ({ style }) => (
                <animated.div style={{ ...style, background: "black" }}>{text}</animated.div>
            )
        setPages([...pages, input_])
    }

    useEffect(() => {
        transRef.start()
    }, [index])

    return (
        <>
            <div className={styles.container}>
                <div className={styles.inner}>
                    <div className={styles.content} onClick={onClick}>
                        {transitions((style, i) => {
                            const Page = pages[i]
                            return <Page style={style} />
                        })}
                    </div>
                </div>
            </div>
        </>
    )
}

export default MainPage
