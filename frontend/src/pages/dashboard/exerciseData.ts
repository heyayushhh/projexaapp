export interface Exercise {
  id: number;
  type: 'SoundRep' | 'WordRep' | 'Interjection' | 'Prolongation' | 'NoStutteredWords';
  difficulty: 'Easy' | 'Medium' | 'Hard';
  level: number;
  sentence: string;
  targetFocus: string;
}

const generateExercises = (): Exercise[] => {
  const types: Exercise['type'][] = ['SoundRep', 'WordRep', 'Interjection', 'Prolongation', 'NoStutteredWords'];
  const difficulties: Exercise['difficulty'][] = ['Easy', 'Medium', 'Hard'];
  const exercises: Exercise[] = [];
  let id = 1;

  const sentences: Record<Exercise['type'], Record<Exercise['difficulty'], string[]>> = {
    SoundRep: {
      Easy: [
        "The bill is on the table.",
        "Please pass the paper to me.",
        "The train ticket is in my bag.",
        "Keep the coffee cup close.",
        "The phone is on silent mode.",
        "My notes are ready for review.",
        "We can meet at ten today.",
        "Take a calm breath and start.",
        "I will speak with a steady pace.",
        "That is a clear plan for now."
      ],
      Medium: [
        "Please bring the report before the meeting begins.",
        "I can explain the plan with clear, calm speech.",
        "Take a steady breath, then start the next sentence.",
        "Keep your lips light and your voice gentle.",
        "The project deadline is close, so we will stay focused.",
        "I will talk at a steady pace and pause when needed.",
        "My priority is clear communication, not speed.",
        "The schedule is flexible, but we should confirm today.",
        "I can present the key points without rushing.",
        "We will review the details and finalize the decision."
      ],
      Hard: [
        "Before we begin, I will briefly summarize the key points for today.",
        "I can speak clearly in discussion by pausing and keeping my airflow steady.",
        "When I feel pressure, I slow down and use gentle starts on important words.",
        "I will explain my decision calmly, even if I need a short pause to plan.",
        "Please provide the final details so I can confirm the timeline and next steps.",
        "I can introduce myself confidently and keep a steady pace through the whole message.",
        "If I get stuck, I will stop, breathe out softly, and restart with a calm voice.",
        "I will share feedback respectfully and focus on solutions, not speed.",
        "During a presentation, I keep my words connected and my breathing relaxed.",
        "I can handle spontaneous questions by pausing briefly and responding clearly."
      ]
    },
    WordRep: {
      Easy: [
        "I am ready to speak now.",
        "This is a simple clear idea.",
        "I can answer in one sentence.",
        "Please give me a moment.",
        "I will keep my speech steady.",
        "I can share my plan today.",
        "That sounds good to me.",
        "I will start with a calm breath.",
        "I can speak with confidence.",
        "I will pause and continue."
      ],
      Medium: [
        "I want to explain this idea clearly and calmly.",
        "Please give me a minute to organize my thoughts.",
        "I can share two key points and then summarize.",
        "We can discuss the details after the meeting.",
        "I will speak slowly so my words stay clear.",
        "Can you repeat the question one more time?",
        "I can answer now, or I can respond in writing.",
        "I will keep a steady rhythm from word to word.",
        "We should confirm the time and location today.",
        "I can describe the steps in a clear order."
      ],
      Hard: [
        "In this discussion, I will stay calm and speak with a steady pace.",
        "I can explain my background, my strengths, and what I am improving.",
        "I will answer in two parts: context first, then the result.",
        "If I need time to think, I will pause without using filler words.",
        "I can present my perspective respectfully and invite your feedback.",
        "I will communicate clearly, even when the topic feels stressful.",
        "I can share a short example to support my point.",
        "Before I respond, I will take a breath and start gently.",
        "I will slow down, keep airflow steady, and continue smoothly.",
        "I can speak naturally in real conversations with short, planned pauses."
      ]
    },
    Interjection: {
      Easy: [
        "I will pause before I answer.",
        "Give me a moment to think.",
        "I can respond in a clear way.",
        "I will take a breath and begin.",
        "I can explain that in a sentence.",
        "I will speak slowly and clearly.",
        "I can start again with a calm voice.",
        "I will continue after a short pause.",
        "I can ask a question now.",
        "I can share my idea clearly."
      ],
      Medium: [
        "Well, I can explain my approach clearly.",
        "Actually, I need a moment to think.",
        "Honestly, I want to respond in a calm way.",
        "Basically, the main point is simple.",
        "So, I will start with the first detail.",
        "Right now, I prefer a slower pace.",
        "In short, I agree with the plan.",
        "To be clear, I will pause and continue.",
        "For now, I will focus on steady speech.",
        "I mean, I can restate that clearly."
      ],
      Hard: [
        "From my perspective, a brief pause helps me respond clearly.",
        "With all due respect, I see this point a little differently.",
        "To be honest, I need a moment to organize my thoughts.",
        "In other words, I will restate the message with clarity.",
        "On the other hand, we can consider a simpler option.",
        "Generally speaking, I prefer to speak at a steady pace.",
        "To be clear, I will answer in two short parts.",
        "If I am not mistaken, the deadline is next week.",
        "As a result, we should confirm the plan today.",
        "For example, I can give one clear reason."
      ]
    },
    Prolongation: {
      Easy: [
        "So, I can start slowly.",
        "Soft speech starts with steady airflow.",
        "Slow, smooth speech feels more natural.",
        "I can focus on steady airflow.",
        "My voice can begin gently.",
        "Now I can continue smoothly.",
        "I can speak with a softer start.",
        "I will slow down and stay relaxed.",
        "Give me a moment to begin.",
        "One phrase at a time is enough."
      ],
      Medium: [
        "So, I will explain the next step clearly.",
        "Start with gentle airflow, then add your voice.",
        "I can answer after I think for a moment.",
        "Focus on a smooth start, not a fast start.",
        "Steady airflow helps me keep speaking forward.",
        "My voice begins softly, then stays consistent.",
        "Slow down slightly before important words.",
        "I will respond with one clear example.",
        "Sometimes I pause to keep my speech smooth.",
        "Follow the rhythm and keep it relaxed."
      ],
      Hard: [
        "So, before we begin, I will summarize the key points.",
        "Steady airflow supports a calm and confident speaking style.",
        "I can take a brief pause and still sound professional.",
        "A gentle start helps reduce tension in difficult moments.",
        "Sometimes I slow down to keep my speech smooth in conversation.",
        "My voice stays steady when I breathe out softly and start gently.",
        "So, I will answer clearly, even under pressure.",
        "I will explain my reasoning step by step.",
        "Focus on flow: pause, breathe, and continue without forcing.",
        "Steady pacing helps me speak naturally in real situations."
      ]
    },
    NoStutteredWords: {
      Easy: [
        "I can speak in a calm way.",
        "My message is clear and simple.",
        "I will pause and then continue.",
        "I can start with a gentle voice.",
        "I will keep a steady pace.",
        "I can share my idea today.",
        "I can take my time to speak.",
        "I will speak with steady airflow.",
        "I can stay relaxed while talking.",
        "I can finish this sentence smoothly."
      ],
      Medium: [
        "I can introduce myself with calm, clear speech.",
        "I will explain the plan in a simple order.",
        "I can speak clearly during a short discussion.",
        "I will pause briefly between ideas and continue.",
        "I can answer questions with a steady pace.",
        "I can share feedback in a respectful tone.",
        "I will keep my words connected and smooth.",
        "I can speak confidently in small group settings.",
        "I will use short pauses to stay organized.",
        "I can communicate my needs clearly and calmly."
      ],
      Hard: [
        "In a real conversation, I can stay calm and speak with steady rhythm.",
        "I can present my work clearly by using short, planned pauses.",
        "I can respond thoughtfully, even when the topic feels stressful.",
        "I will speak naturally and keep moving forward, even if I stutter.",
        "I can explain my decision with clarity and a confident tone.",
        "I can handle spontaneous questions by pausing briefly and responding clearly.",
        "I can share my perspective respectfully and invite feedback.",
        "I will slow down, keep airflow steady, and maintain control.",
        "I can communicate professionally in meetings and interviews.",
        "I can speak with confidence and clear intent in real situations."
      ]
    }
  };

  types.forEach(type => {
    difficulties.forEach(diff => {
      const targetSentences = sentences[type][diff];
      targetSentences.forEach((sentence, index) => {
        exercises.push({
          id: id++,
          type,
          difficulty: diff,
          level: index + 1,
          sentence,
          targetFocus: getTargetFocus(type)
        });
      });
    });
  });

  return exercises;
};

const getTargetFocus = (type: Exercise['type']): string => {
  switch (type) {
    case 'SoundRep': return "Focus on light contact and smooth sound transition.";
    case 'WordRep': return "Maintain steady rhythm between words.";
    case 'Interjection': return "Focus on pausing instead of using filler words.";
    case 'Prolongation': return "Gentle onset and controlled airflow.";
    case 'NoStutteredWords': return "Maintain continuous phonation and natural flow.";
    default: return "Focus on clear and relaxed speech.";
  }
};

export const EXERCISES = generateExercises();
