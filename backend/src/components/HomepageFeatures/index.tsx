import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.SVGProps<SVGSVGElement>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Spec-Driven Development',
    Svg: require('@site/static/img/spec-driven-icon.svg').default,
    description: (
      <>
        Transform requirements into precise specifications with automated
        documentation, ensuring consistency between planning and implementation.
        Generate PHRs and ADRs automatically during development.
      </>
    ),
  },
  {
    title: 'Automated Implementation',
    Svg: require('@site/static/img/implementation-icon.svg').default,
    description: (
      <>
        Execute tasks directly from specifications with intelligent task routing,
        ensuring every implementation matches the documented requirements.
        Built-in validation and testing at every step.
      </>
    ),
  },
  {
    title: 'Architecture Blueprint',
    Svg: require('@site/static/img/architecture-icon.svg').default,
    description: (
      <>
        Visual architecture design with layer-based structure. From hardware
        specifications to software patterns, build robust systems that scale.
        Document decisions with comprehensive ADR tracking.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}