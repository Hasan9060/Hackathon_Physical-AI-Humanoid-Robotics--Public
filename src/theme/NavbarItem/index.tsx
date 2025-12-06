import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import AuthNavButton from '@site/src/components/AuthProvider/AuthNavButton';

export default function NavbarItemWrapper(props: any): JSX.Element {
    if (props.type === 'custom-auth') {
        return <AuthNavButton />;
    }
    return <NavbarItem {...props} />;
}
