import ThemeToggle from './ThemeToggle';
import { useThemeStore } from '../store/themeStore';
import { useNavigate } from 'react-router-dom';

interface NavbarProps {
  onNavigate: (page: string) => void;
  currentPage: string;
}

const Navbar = ({ onNavigate, currentPage }: NavbarProps) => {
  const { isDark, isAuthenticated, logout } = useThemeStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
    onNavigate('landing');
  };

  const handleLogoClick = () => {
    navigate('/');
    onNavigate('landing');
  };

  const handleDashboardClick = () => {
    navigate('/dashboard');
    onNavigate('dashboard');
  };

  const handleAuthClick = () => {
    navigate('/auth');
    onNavigate('auth');
  };

  return (
    <nav className={`flex items-center justify-between px-8 py-4 backdrop-blur-md sticky top-0 z-50 border-b transition-all duration-500 ${
      isDark 
        ? 'bg-black/30 border-white/10 text-white' 
        : 'bg-white/30 border-black/5 text-[#111]'
    }`}>
      <div 
        className="text-2xl font-bold cursor-pointer transition-colors duration-500"
        onClick={handleLogoClick}
      >
        VocaCare
      </div>
      
      <div className="flex items-center space-x-8">
        <div className={`flex items-center space-x-6 transition-colors duration-500 ${isDark ? 'text-gray-300' : 'text-[#444]'}`}>
          <button className="hover:text-red-500 dark:hover:text-red-400 transition-colors cursor-pointer font-medium" onClick={() => onNavigate('why')}>Why</button>
          <button className="hover:text-red-500 dark:hover:text-red-400 transition-colors cursor-pointer font-medium" onClick={() => onNavigate('about')}>About</button>
          <button className="hover:text-red-500 dark:hover:text-red-400 transition-colors cursor-pointer font-medium" onClick={() => onNavigate('feedback')}>Feedback</button>
        </div>
        
        <div className="flex items-center space-x-4 border-l border-black/10 dark:border-white/10 pl-8">
          {isAuthenticated ? (
            <>
              {currentPage !== 'dashboard' && (
                <button 
                  className={`btn btn-sm rounded-full px-6 transition-all duration-300 shadow-md hover:scale-105 active:scale-95 ${
                    isDark ? 'btn-primary' : 'bg-[#FF2E2E] hover:bg-[#E02929] border-none text-white shadow-red-500/20'
                  }`}
                  onClick={handleDashboardClick}
                >
                  Dashboard
                </button>
              )}
              <button 
                className={`btn btn-ghost btn-sm transition-colors duration-500 font-medium ${isDark ? 'text-gray-300' : 'text-[#444]'}`}
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              {currentPage !== 'auth' && (
                <button 
                  className={`btn btn-sm rounded-full px-6 transition-all duration-300 shadow-md hover:scale-105 active:scale-95 ${
                    isDark ? 'btn-primary' : 'bg-[#FF2E2E] hover:bg-[#E02929] border-none text-white shadow-red-500/20'
                  }`}
                  onClick={handleAuthClick}
                >
                  LOGIN / SIGN IN
                </button>
              )}
            </>
          )}
          
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
