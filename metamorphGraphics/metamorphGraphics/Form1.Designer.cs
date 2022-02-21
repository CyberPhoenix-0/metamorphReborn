namespace metamorphGraphics
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage1 = new System.Windows.Forms.TabPage();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.addressBox = new System.Windows.Forms.TextBox();
            this.websiteTitle = new System.Windows.Forms.TextBox();
            this.scanButton = new System.Windows.Forms.Button();
            this.tabControl1.SuspendLayout();
            this.SuspendLayout();
            // 
            // tabControl1
            // 
            this.tabControl1.Controls.Add(this.tabPage1);
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Location = new System.Drawing.Point(18, 13);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(1021, 381);
            this.tabControl1.TabIndex = 0;
            // 
            // tabPage1
            // 
            this.tabPage1.BackColor = System.Drawing.Color.FromArgb(((int) (((byte) (41)))), ((int) (((byte) (44)))), ((int) (((byte) (45)))));
            this.tabPage1.Location = new System.Drawing.Point(4, 22);
            this.tabPage1.Name = "tabPage1";
            this.tabPage1.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage1.Size = new System.Drawing.Size(1013, 355);
            this.tabPage1.TabIndex = 0;
            this.tabPage1.Text = "tabPage1";
            // 
            // tabPage2
            // 
            this.tabPage2.Location = new System.Drawing.Point(4, 22);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(1013, 355);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "tabPage2";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // addressBox
            // 
            this.addressBox.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte) (0)));
            this.addressBox.Location = new System.Drawing.Point(18, 436);
            this.addressBox.Name = "addressBox";
            this.addressBox.Size = new System.Drawing.Size(260, 26);
            this.addressBox.TabIndex = 1;
            // 
            // websiteTitle
            // 
            this.websiteTitle.BackColor = System.Drawing.Color.FromArgb(((int) (((byte) (41)))), ((int) (((byte) (44)))), ((int) (((byte) (45)))));
            this.websiteTitle.BorderStyle = System.Windows.Forms.BorderStyle.None;
            this.websiteTitle.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte) (0)));
            this.websiteTitle.ForeColor = System.Drawing.Color.FromArgb(((int) (((byte) (0)))), ((int) (((byte) (192)))), ((int) (((byte) (192)))));
            this.websiteTitle.Location = new System.Drawing.Point(18, 411);
            this.websiteTitle.Name = "websiteTitle";
            this.websiteTitle.Size = new System.Drawing.Size(260, 19);
            this.websiteTitle.TabIndex = 2;
            this.websiteTitle.Text = "Website To Scan";
            this.websiteTitle.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.websiteTitle.Enter += new System.EventHandler(this.textBox2_Enter);
            // 
            // scanButton
            // 
            this.scanButton.Location = new System.Drawing.Point(294, 436);
            this.scanButton.Name = "scanButton";
            this.scanButton.Size = new System.Drawing.Size(105, 25);
            this.scanButton.TabIndex = 3;
            this.scanButton.Text = "Scan Website";
            this.scanButton.UseVisualStyleBackColor = true;
            this.scanButton.Click += new System.EventHandler(this.scanButton_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int) (((byte) (40)))), ((int) (((byte) (41)))), ((int) (((byte) (45)))));
            this.ClientSize = new System.Drawing.Size(1106, 530);
            this.Controls.Add(this.scanButton);
            this.Controls.Add(this.websiteTitle);
            this.Controls.Add(this.addressBox);
            this.Controls.Add(this.tabControl1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.tabControl1.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        private System.Windows.Forms.Button scanButton;

        private System.Windows.Forms.TextBox websiteTitle;

        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.TextBox addressBox;

        #endregion
    }
}