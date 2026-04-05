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
        "Pat the pet.", "Big blue box.", "Ten tiny toys.", "Red rubber ball.", "Six silly songs.",
        "Pink paper pig.", "Good green grass.", "Hot hard hat.", "Cold clear cup.", "Fast flat feet."
      ],
      Medium: [
        "Peter Piper picked.", "Betty Botter bought.", "She sells seashells.", "Proper copper pot.", "Greek grapes grow.",
        "Toy boat, toy boat.", "Truly rural road.", "Rubber baby buggy.", "Six slippery snails.", "Clean clams crash."
      ],
      Hard: [
        "Purple paper people pick.", "Seven selfish shellfish sleep.", "Unique New York roads.", "Mixed biscuits in a box.", "A loyal warrior learns.",
        "Red lory, yellow lory.", "Specific Pacific ocean.", "Thieving thugs think.", "Black background, brown background.", "Friendly frankly flying."
      ]
    },
    WordRep: {
      Easy: [
        "The cat sat.", "Go to bed.", "I like cake.", "Sun is hot.", "Dog can run.",
        "Big red car.", "Play with ball.", "See the moon.", "Look at me.", "Time to eat."
      ],
      Medium: [
        "I want to go.", "She has a book.", "They play outside.", "We like to swim.", "He runs very fast.",
        "The water is cold.", "My friend is nice.", "Can you help me?", "Where is the key?", "It is raining now."
      ],
      Hard: [
        "I wonder why he went.", "The weather is very nice.", "Sometimes I think about life.", "Education is very important.", "Communication helps everyone.",
        "Understanding takes some time.", "Professional development matters.", "Technological advancement continues.", "Environmental protection is key.", "Psychological factors are complex."
      ]
    },
    Interjection: {
      Easy: [
        "Hello there.", "How are you?", "Yes I am.", "No not yet.", "Wait for me.",
        "Please sit down.", "Thanks a lot.", "Excuse me now.", "Good morning all.", "See you soon."
      ],
      Medium: [
        "Well, I think so.", "Actually, it is true.", "Basically, we are done.", "Honestly, I don't know.", "Literally, it happened.",
        "Seriously, stop that.", "Basically, let's go.", "Frankly, I am tired.", "Totally, I agree.", "Maybe, we can try."
      ],
      Hard: [
        "As a matter of fact.", "In my humble opinion.", "To be perfectly honest.", "If I am not mistaken.", "With all due respect.",
        "Needless to say that.", "From my perspective.", "Generally speaking now.", "In other words today.", "On the other hand."
      ]
    },
    Prolongation: {
      Easy: [
        "Smile at sun.", "Slow small steps.", "Star stays still.", "Stone stands strong.", "Snake slides slow.",
        "Snow smells sweet.", "Sky shows stars.", "Sea sounds soft.", "Sleep soundly now.", "Stay safe soon."
      ],
      Medium: [
        "Slowly slide down.", "Slightly small snacks.", "Slippery slope slide.", "Starting small steps.", "Simple silver spoon.",
        "Sailing silent seas.", "Singing sweet songs.", "Searching small spaces.", "Sending short signals.", "Sitting still soon."
      ],
      Hard: [
        "Systematic speech sessions.", "Significantly support stability.", "Stable sounding syllables.", "Starting strong sentences.", "Simple sounds support speech.",
        "Speaking slowly supports success.", "Successful speech starts small.", "Stability supports sounding strong.", "Significantly simple sounds.", "Stable speech starts slowly."
      ]
    },
    NoStutteredWords: {
      Easy: [
        "I love books.", "The sky is blue.", "Birds can fly.", "Dogs like bones.", "Fish can swim.",
        "Apples are red.", "Grass is green.", "Water is clear.", "Fire is hot.", "Ice is cold."
      ],
      Medium: [
        "Artificial intelligence works.", "Model processed data.", "High accuracy achieved.", "Learning takes practice.", "Technology is helpful.",
        "Future is bright.", "Innovation drives growth.", "Science is amazing.", "Knowledge is power.", "Reading expands mind."
      ],
      Hard: [
        "Continuous clinical improvement.", "Communication requires practice.", "Dedicated effort counts.", "Consistent daily sessions.", "Professional growth happens.",
        "Advanced analysis methods.", "Systematic approach works.", "Clinical grade results.", "Premium quality system.", "Advanced speech tools."
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
