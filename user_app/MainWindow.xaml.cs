using System.ComponentModel;
using System.Drawing;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using System.Windows.Media.Animation;

namespace Sim_Racing_Telemetry
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        /// <summary>
        /// The currently open menu
        /// </summary>
        private static int currentMenu = 0;

        /// <summary>
        /// Used to store all the main grids
        /// </summary> 
        private static List<Grid> mainGrids = new List<Grid>();

        /// <summary>
        /// Used to store all the buttons in the side bar
        /// </summary>
        private static List<Button> menuButtons = new List<Button>();

        public MainWindow()
        {
            InitializeComponent();

            // Populate mainGrids
            mainGrids = new List<Grid>
            {
                Grd_Home,
                Grd_Setup,
                Grd_Telemetry
            };

            // Populate menuButton
            menuButtons = new List<Button>
            {
                Btn_Home,
                Btn_Setup,
                Btn_Telemetry
            };

            // Open the main menu on init
            ResetGridVisibility(this);
            Grd_Main.Visibility = Visibility.Visible;
        }


        /// <summary>
        /// Resets the visibility of all the grids.
        /// </summary>
        /// <param name="instance">The instance of the MainWindow</param>
        private static void ResetGridVisibility(MainWindow instance)
        {
            foreach (var grid in mainGrids)
            {
                grid.Visibility = Visibility.Collapsed;
            }
        }

        #region Setup

        /// <summary>
        /// Used to store all the grids used in the setup process.
        /// </summary>
        private static List<Grid> setupGrids = new List<Grid>();

        /// <summary>
        /// Used to store all the progress rectangles for the setup process.
        /// </summary>
        private static List<System.Windows.Shapes.Rectangle> progressBars = new List<System.Windows.Shapes.Rectangle>();

        /// <summary>
        /// This counter is used to track the current step in the setup process.
        /// </summary>
        private static int currentSetupStep = -1; // -1 indicates no step has been started yet

        /// <summary>
        /// The total number of setup steps.
        /// </summary>
        private const int totalSetupSteps = 4;

        /// <summary>
        /// Called to start the setup process.
        /// </summary>
        /// <param name="instance">The instance of the MainWindow.</param>
        private static void SetupTrigger(MainWindow instance)
        {

            // Add the setup grids to the list
            setupGrids = new List<Grid>
            {
                instance.Grd_Setup_DeviceType,
                instance.Grd_Setup_DeviceIP,
                instance.Grd_Setup_Customization,
                instance.Grd_Setup_Finished
            };

            // Add the progress bars to the list
            progressBars = new List<System.Windows.Shapes.Rectangle>
            {
                instance.Rct_Setup_Progress0,
                instance.Rct_Setup_Progress1,
                instance.Rct_Setup_Progress2,
                instance.Rct_Setup_Progress3
            };

            // Grey out all of the bars
            foreach (var bar in progressBars)
            {
                bar.Fill = (SolidColorBrush)Application.Current.Resources["Background"];
            }
        }

        /// <summary>
        /// Hide all the setup grids
        /// </summary>
        private static void ResetSetupGridVisibility()
        {
            foreach (var grid in setupGrids)
            {
                grid.Visibility = Visibility.Collapsed;
            }
        }

        private void Btn_Setup_Next_Click(object sender, RoutedEventArgs e)
        {
            if (currentSetupStep == -1)
            {
                SetupTrigger(this); // Trigger setup if not already started
                currentSetupStep = 0;
            }

            if (currentSetupStep > totalSetupSteps)
            {
                // Handle setup process completion
                ResetGridVisibility(this);
                ResetSetupGridVisibility();
                Grd_Setup.Visibility = Visibility.Visible;
                currentSetupStep = -1;
                Btn_Setup_Next.Content = "Start"; // Reset button text to "Start Setup"

                // Reset all progress bars to grey
                foreach (var bar in progressBars)
                {
                    bar.Fill = (SolidColorBrush)Application.Current.Resources["Background"];
                }

                //TODO Actually save the setup data here
            }
            else if (currentSetupStep <= totalSetupSteps)
            {
                // Show the next step
                if (currentSetupStep != totalSetupSteps)
                {
                    ResetSetupGridVisibility();
                    setupGrids[currentSetupStep].Visibility = Visibility.Visible;
                    Btn_Setup_Next.Content = "Next"; // Reset button text to "Next"
                }
                else
                {
                    Btn_Setup_Next.Content = "Finish"; // Change button text to "Finish" on the last step
                }

                // Set the last step's progress bar part to indicate the step's completion
                if (currentSetupStep != 0)
                {
                    var to = Application.Current.Resources["Accent"] as SolidColorBrush;
                    if (to == null)
                    {
                        return;
                    }

                    var from = progressBars[currentSetupStep - 1].Fill as SolidColorBrush;
                    if (from == null || from.Color == to.Color)
                    {
                        return;
                    }

                    // Assign a new brush instance to avoid animating a shared resource
                    var newBrush = new SolidColorBrush(from.Color);
                    progressBars[currentSetupStep - 1].Fill = newBrush;

                    var animation = new ColorAnimation
                    {
                        To = to.Color,
                        Duration = TimeSpan.FromSeconds(0.25),
                        EasingFunction = new CubicEase { EasingMode = EasingMode.EaseInOut }
                    };
                    newBrush.BeginAnimation(SolidColorBrush.ColorProperty, animation);
                }

                currentSetupStep++;
            }
        }

        #endregion

        #region Side Bar Buttons

        /// <summary>
        /// Set the current selected menu's button to a different color to indicate the selection
        /// </summary>
        /// <param name="instance">The instance of MainWindow</param>
        private static void MenuButtonColorSet(MainWindow instance)
        {
            // Reset former menu button color
            foreach (var button in menuButtons)
            {
                var textBrush = Application.Current.Resources["Text"] as SolidColorBrush;
                if (textBrush == null)
                {
                    continue;
                }

                var currentBrush = button.Foreground as SolidColorBrush;
                if (currentBrush == null || currentBrush.Color == textBrush.Color)
                {
                    continue;
                }

                // Assign a new brush instance to avoid animating a shared resource
                var newBrush = new SolidColorBrush(currentBrush.Color);
                button.Foreground = newBrush;

                var animation = new ColorAnimation
                {
                    To = textBrush.Color,
                    Duration = TimeSpan.FromSeconds(0.25),
                    EasingFunction = new CubicEase { EasingMode = EasingMode.EaseInOut }
                };
                newBrush.BeginAnimation(SolidColorBrush.ColorProperty, animation);
            }

            // Set the now opened menu's button color
            var highlightBrush = Application.Current.Resources["Highlight"] as SolidColorBrush;
            if (highlightBrush == null)
            {
                return;
            }

            var selectedButton = menuButtons[currentMenu];
            var selectedBrush = selectedButton.Foreground as SolidColorBrush;
            if (selectedBrush == null)
            {
                return;
            }

            // Assign a new brush instance for animation
            var newSelectedBrush = new SolidColorBrush(selectedBrush.Color);
            selectedButton.Foreground = newSelectedBrush;

            var animationBrush = new ColorAnimation
            {
                To = highlightBrush.Color,
                Duration = TimeSpan.FromSeconds(0.25),
                EasingFunction = new CubicEase { EasingMode = EasingMode.EaseInOut }
            };
            newSelectedBrush.BeginAnimation(SolidColorBrush.ColorProperty, animationBrush);
        }

        private void Btn_Home_Click(object sender, RoutedEventArgs e)
        {
            ResetGridVisibility(this);
            currentMenu = 0;
            MenuButtonColorSet(this);
            Grd_Home.Visibility = Visibility.Visible;
        }

        private void Btn_Setup_Click(object sender, RoutedEventArgs e)
        {
            ResetGridVisibility(this);
            currentMenu = 1;
            MenuButtonColorSet(this);
            SetupTrigger(this);
            Btn_Setup_Next.Content = "Start";
            Grd_Setup.Visibility = Visibility.Visible;
        }

        private void Btn_Telemetry_Click(object sender, RoutedEventArgs e)
        {
            ResetGridVisibility(this);
            currentMenu = 2;
            MenuButtonColorSet(this);
            Grd_Telemetry.Visibility = Visibility.Visible;
        }

        #endregion
    }
}