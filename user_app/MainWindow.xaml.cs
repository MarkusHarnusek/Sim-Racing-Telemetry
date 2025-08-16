using System.Drawing;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace Sim_Racing_Telemetry
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
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

            // Fill in all the grids
            mainGrids = new List<Grid>
            {
                Grd_Main,
                Grd_Setup
            };

            // TODO Add side bar buttons
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
            ResetGridVisibility(instance);
            instance.Grd_Setup.Visibility = Visibility.Visible;

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
                bar.Fill = (SolidColorBrush)Application.Current.Resources["Greyed"];
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

            if (currentSetupStep == totalSetupSteps )
            {
                ResetGridVisibility(this);
                ResetSetupGridVisibility();
                Grd_Setup.Visibility = Visibility.Visible;
                currentSetupStep = -1;

                // TODO Actually save the setup data here
            }
            else if (currentSetupStep < totalSetupSteps)
            {
                ResetSetupGridVisibility();
                setupGrids[currentSetupStep].Visibility = Visibility.Visible;

                if (currentSetupStep != 0)
                {
                    progressBars[currentSetupStep - 1].Fill = (SolidColorBrush)Application.Current.Resources["Foreground"];
                }

                currentSetupStep++;
            }
        }

        #endregion

    }
}