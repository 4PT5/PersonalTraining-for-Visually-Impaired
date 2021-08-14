import React from 'react';
import {
    Grommet as GrommetIcon,
    Github
} from 'grommet-icons';
import styles from './Footer.module.css';

import { Anchor, Box, Footer, grommet, Grommet, Main, Text } from 'grommet';

const Media = () => (
    <Box direction="row" gap="xxsmall" justify="center">
        <Anchor
            a11yTitle="Share feedback on Github"
            href="https://github.com/4PT5/PersonalTraining-for-Visually-Impaired"
            icon={<Github color="brand" />}
        />
    </Box>
);

function FooterMedia() {
    return (
        <div className={styles.footer}>
            <Grommet theme={grommet}>
                <Footer background="light-4" pad="small">
                    <Box align="center" direction="row" gap="xsmall">
                        <GrommetIcon color="brand" size="medium" />
                        <Text alignSelf="center" color="brand" size="small">
                            4PT5
                        </Text>
                    </Box>
                    <Media />
                    <Text textAlign="center" size="xsmall">
                        ©Copyright
                    </Text>
                </Footer>
            </Grommet>
        </div>
    )
}

export default FooterMedia;