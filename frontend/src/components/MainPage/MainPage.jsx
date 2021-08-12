import React, { useState, useCallback, CSSProperties, useEffect } from 'react'
import { useTransition, animated, AnimatedProps, useSpringRef } from '@react-spring/web'
import styles from './MainPage.module.css';

const pages = [
    ({ style }) => React.createElement(animated.div, { style: Object.assign(Object.assign({}, style), { background: 'lightpink' }) }, "A"),
    ({ style }) => React.createElement(animated.div, { style: Object.assign(Object.assign({}, style), { background: 'lightblue' }) }, "B"),
    ({ style }) => React.createElement(animated.div, { style: Object.assign(Object.assign({}, style), { background: 'lightgreen' }) }, "C"),
];

function MainPage() {

    const [index, setIndex] = useState(0);
    const onClick = useCallback(() => setIndex(state => (state + 1) % 3), [])
    const transRef = useSpringRef()
    const transitions = useTransition(index, {
        ref: transRef,
        keys: null,
        from: { opacity: 0, transform: 'translate3d(100%,0,0)' },
        enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
        leave: { opacity: 0, transform: 'translate3d(-50%,0,0)' },
    })

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
