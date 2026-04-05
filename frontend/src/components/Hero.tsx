import { motion } from 'framer-motion';
import { useThemeStore } from '../store/themeStore';

interface HeroProps {
  onStart: () => void;
}

const Hero = ({ onStart }: HeroProps) => {
  const { isDark } = useThemeStore();

  return (
    <div className="flex flex-col justify-center min-h-[90vh] px-[8%] md:px-[12%]">
      <motion.div
        initial={{ opacity: 0, x: -30 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 1, ease: "easeOut" }}
        className="max-w-2xl"
      >
        <h1 className={`text-6xl md:text-8xl font-bold leading-[1.1] mb-12 tracking-tight transition-colors duration-500 ${
          isDark ? 'text-white' : 'text-[#111]'
        }`}>
          Analyze Your <br />
          Speech with <br />
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#FF2E2E] to-[#FF8080]">AI Precision</span>
        </h1>
        
        <p className={`text-xl md:text-2xl mb-14 max-w-[500px] leading-relaxed transition-colors duration-500 font-medium ${
          isDark ? 'text-gray-300' : 'text-[#444]'
        }`}>
          Medical-grade deep learning technology designed to track, analyze, and help improve speech patterns with clinical accuracy.
        </p>
        
        <motion.button
          whileHover={{ scale: 1.05, boxShadow: isDark ? '0 20px 40px -10px rgba(255,46,46,0.4)' : '0 20px 40px -10px rgba(255,46,46,0.2)' }}
          whileTap={{ scale: 0.96 }}
          onClick={onStart}
          className="bg-[#FF2E2E] hover:bg-[#E02929] text-white font-bold py-5 px-14 rounded-full text-xl shadow-2xl shadow-red-500/30 transition-all duration-300 border-none cursor-pointer"
        >
          Let's Start
        </motion.button>
      </motion.div>
    </div>
  );
};

export default Hero;
