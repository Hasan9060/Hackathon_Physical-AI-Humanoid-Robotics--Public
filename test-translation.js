// Test script for translation API
// Run with: node test-translation.js

const API_URL = 'http://localhost:8000';

async function testTranslation() {
  console.log('Testing translation API...\n');

  // Test 1: Health check
  try {
    const healthResponse = await fetch(`${API_URL}/api/v1/translation-stats`);
    const healthData = await healthResponse.json();
    console.log('✓ Health check passed:', healthData);
  } catch (error) {
    console.log('✗ Health check failed:', error.message);
    return;
  }

  // Test 2: Simple translation
  try {
    const translateResponse = await fetch(`${API_URL}/api/v1/translate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: 'Hello world! This is a test of the translation system.',
        target_lang: 'ur',
        source_lang: 'en',
      }),
    });

    if (translateResponse.ok) {
      const translateData = await translateResponse.json();
      console.log('\n✓ Translation successful:');
      console.log('  Original:', translateData.source_lang);
      console.log('  Target:', translateData.target_lang);
      console.log('  Chunks:', translateData.chunks_processed);
      console.log('  Provider:', translateData.provider);
      console.log('  Cached:', translateData.cached);
      console.log('  Result:', translateData.translated_text);
    } else {
      console.log('\n✗ Translation failed:', translateResponse.statusText);
    }
  } catch (error) {
    console.log('\n✗ Translation error:', error.message);
  }

  // Test 3: Chapter translation with progress
  try {
    const chapterText = `
      # Introduction to Robotics

      Robotics is an interdisciplinary field that combines computer science, engineering, and technology.
      It involves the design, construction, operation, and use of robots.

      The goal of robotics is to create machines that can help and assist humans.
      Robots can be used in various applications including manufacturing, healthcare,
      space exploration, and more.

      In this course, we will explore the fundamentals of robotics and learn
      how to build and program robots for various applications.
    `;

    const chapterResponse = await fetch(`${API_URL}/api/v1/translate-chapter`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: chapterText,
        target_lang: 'ur',
        source_lang: 'en',
        chunk_size: 100, // Small chunks for testing
      }),
    });

    if (chapterResponse.ok) {
      const chapterData = await chapterResponse.json();
      console.log('\n✓ Chapter translation started:');
      console.log('  Task ID:', chapterData.task_id);
      console.log('  Message:', chapterData.message);

      // Poll for progress
      let completed = false;
      let attempts = 0;
      const maxAttempts = 30;

      while (!completed && attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds

        const progressResponse = await fetch(`${API_URL}/api/v1/translate-progress/${chapterData.task_id}`);
        if (progressResponse.ok) {
          const progressData = await progressResponse.json();
          console.log(`\n  Progress check ${attempts + 1}:`);
          console.log('    Status:', progressData.status);
          console.log('    Progress:', Math.round(progressData.progress * 100), '%');
          console.log('    Chunk:', progressData.current_chunk, '/', progressData.total_chunks);

          if (progressData.status === 'completed') {
            console.log('\n✓ Chapter translation completed!');
            console.log('  Translated text preview:');
            console.log('  ', progressData.translated_text.substring(0, 200) + '...');
            completed = true;
          } else if (progressData.status === 'failed') {
            console.log('\n✗ Chapter translation failed:', progressData.error);
            completed = true;
          }
        }

        attempts++;
      }

      if (!completed) {
        console.log('\n✗ Chapter translation timed out');
      }
    } else {
      console.log('\n✗ Chapter translation failed to start:', chapterResponse.statusText);
    }
  } catch (error) {
    console.log('\n✗ Chapter translation error:', error.message);
  }

  console.log('\nTest completed!');
}

// Run the test
testTranslation().catch(console.error);