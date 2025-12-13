import React from 'react';
import NavbarItem from '@theme/NavbarItem';
import LanguageSelector from '@site/src/components/LanguageSelector';

export default function LanguageSelectorItem() {
  return (
    <NavbarItem
      className="navbar__item"
      component={LanguageSelector}
    />
  );
}