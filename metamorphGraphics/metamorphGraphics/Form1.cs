using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace metamorphGraphics
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }


        #region ItemsReadableOnly

        private void textBox2_Enter(object sender, EventArgs e)
        {
            websiteTitle.Enabled = false;
            websiteTitle.Enabled = true;
        }

        #endregion

        private void scanButton_Click(object sender, EventArgs e)
        {
            throw new System.NotImplementedException();
            //Implement All scanning modules
        }
    }
}