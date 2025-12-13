import React from 'react';
import Layout from '@theme-original/Layout';
import { RAGChatbot } from '@site/src/components/RAGChatbot';

export default function LayoutWrapper(props: any): JSX.Element {
  return (
    <>
      <Layout {...props} />
      <RAGChatbot apiBaseUrl="http://localhost:8000/api/v1" />
    </>
  );
}