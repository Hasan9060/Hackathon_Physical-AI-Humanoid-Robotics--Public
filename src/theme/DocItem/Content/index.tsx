
import React from 'react';
import Content from '@theme-original/DocItem/Content';
import ScrollIndicator from '@site/src/components/ScrollIndicator';

export default function ContentWrapper(props: any): JSX.Element {
    return (
        <>
            <ScrollIndicator />
            <Content {...props} />
        </>
    );
}
