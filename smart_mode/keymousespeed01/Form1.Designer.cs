namespace keymousespeed01
{
    partial class Form1
    {
        /// <summary>
        /// Erforderliche Designervariable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Verwendete Ressourcen bereinigen.
        /// </summary>
        /// <param name="disposing">True, wenn verwaltete Ressourcen gelöscht werden sollen; andernfalls False.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Vom Windows Form-Designer generierter Code

        /// <summary>
        /// Erforderliche Methode für die Designerunterstützung.
        /// Der Inhalt der Methode darf nicht mit dem Code-Editor geändert werden.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.CheckBoxWinPlainText = new System.Windows.Forms.CheckBox();
            this.hideButton = new System.Windows.Forms.Button();
            this.exitButton = new System.Windows.Forms.Button();
            this.checkBoxPlainText = new System.Windows.Forms.CheckBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.KeyboardTypeLabel = new System.Windows.Forms.Label();
            this.KeyboardLayoutLabel = new System.Windows.Forms.Label();
            this.ActiveWinLabel = new System.Windows.Forms.Label();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.label4 = new System.Windows.Forms.Label();
            this.trayIcon = new System.Windows.Forms.NotifyIcon(this.components);
            this.FileNameLabel = new System.Windows.Forms.Label();
            this.textBoxLogFileName = new System.Windows.Forms.TextBox();
            this.checkBoxMouseEvents = new System.Windows.Forms.CheckBox();
            this.checkBoxKeyEvents = new System.Windows.Forms.CheckBox();
            this.SuspendLayout();
            // 
            // CheckBoxWinPlainText
            // 
            this.CheckBoxWinPlainText.AutoSize = true;
            this.CheckBoxWinPlainText.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.CheckBoxWinPlainText.Location = new System.Drawing.Point(436, 60);
            this.CheckBoxWinPlainText.Name = "CheckBoxWinPlainText";
            this.CheckBoxWinPlainText.Size = new System.Drawing.Size(316, 29);
            this.CheckBoxWinPlainText.TabIndex = 2;
            this.CheckBoxWinPlainText.Text = "Record window titles in plain text";
            this.CheckBoxWinPlainText.UseVisualStyleBackColor = true;
            // 
            // hideButton
            // 
            this.hideButton.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.hideButton.Location = new System.Drawing.Point(16, 108);
            this.hideButton.Name = "hideButton";
            this.hideButton.Size = new System.Drawing.Size(797, 76);
            this.hideButton.TabIndex = 3;
            this.hideButton.Text = "Hide this Application in the Background";
            this.hideButton.UseVisualStyleBackColor = true;
            this.hideButton.Click += new System.EventHandler(this.hideButton_Click);
            // 
            // exitButton
            // 
            this.exitButton.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.exitButton.Location = new System.Drawing.Point(644, 304);
            this.exitButton.Name = "exitButton";
            this.exitButton.Size = new System.Drawing.Size(169, 52);
            this.exitButton.TabIndex = 4;
            this.exitButton.Text = "Exit Application";
            this.exitButton.UseVisualStyleBackColor = true;
            this.exitButton.Click += new System.EventHandler(this.exitButton_Click);
            // 
            // checkBoxPlainText
            // 
            this.checkBoxPlainText.AutoSize = true;
            this.checkBoxPlainText.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxPlainText.Location = new System.Drawing.Point(16, 60);
            this.checkBoxPlainText.Name = "checkBoxPlainText";
            this.checkBoxPlainText.Size = new System.Drawing.Size(352, 29);
            this.checkBoxPlainText.TabIndex = 1;
            this.checkBoxPlainText.Text = "Record keys in plain text (keylogger)";
            this.checkBoxPlainText.UseVisualStyleBackColor = true;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 304);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(118, 20);
            this.label1.TabIndex = 5;
            this.label1.Text = "Keyboard Type:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 336);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(132, 20);
            this.label2.TabIndex = 6;
            this.label2.Text = "Keyboard Layout:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 275);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(116, 20);
            this.label3.TabIndex = 7;
            this.label3.Text = "Active Window:";
            // 
            // KeyboardTypeLabel
            // 
            this.KeyboardTypeLabel.AutoSize = true;
            this.KeyboardTypeLabel.Location = new System.Drawing.Point(139, 304);
            this.KeyboardTypeLabel.Name = "KeyboardTypeLabel";
            this.KeyboardTypeLabel.Size = new System.Drawing.Size(130, 20);
            this.KeyboardTypeLabel.TabIndex = 8;
            this.KeyboardTypeLabel.Text = "SampleKeyboard";
            // 
            // KeyboardLayoutLabel
            // 
            this.KeyboardLayoutLabel.AutoSize = true;
            this.KeyboardLayoutLabel.Location = new System.Drawing.Point(139, 336);
            this.KeyboardLayoutLabel.Name = "KeyboardLayoutLabel";
            this.KeyboardLayoutLabel.Size = new System.Drawing.Size(111, 20);
            this.KeyboardLayoutLabel.TabIndex = 9;
            this.KeyboardLayoutLabel.Text = "SampleLayout";
            // 
            // ActiveWinLabel
            // 
            this.ActiveWinLabel.AutoSize = true;
            this.ActiveWinLabel.Location = new System.Drawing.Point(139, 275);
            this.ActiveWinLabel.Name = "ActiveWinLabel";
            this.ActiveWinLabel.Size = new System.Drawing.Size(119, 20);
            this.ActiveWinLabel.TabIndex = 10;
            this.ActiveWinLabel.Text = "SampleWindow";
            // 
            // timer1
            // 
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(13, 387);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(36, 20);
            this.label4.TabIndex = 11;
            this.label4.Text = "test";
            // 
            // trayIcon
            // 
            this.trayIcon.BalloonTipIcon = System.Windows.Forms.ToolTipIcon.Info;
            this.trayIcon.BalloonTipText = "Ballon Text";
            this.trayIcon.BalloonTipTitle = "Ballon Title";
            this.trayIcon.Icon = ((System.Drawing.Icon)(resources.GetObject("trayIcon.Icon")));
            this.trayIcon.Text = "TypingSpeedLogger";
            this.trayIcon.Visible = true;
            this.trayIcon.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.trayIcon_MouseDoubleClick);
            // 
            // FileNameLabel
            // 
            this.FileNameLabel.AutoSize = true;
            this.FileNameLabel.Location = new System.Drawing.Point(12, 219);
            this.FileNameLabel.Name = "FileNameLabel";
            this.FileNameLabel.Size = new System.Drawing.Size(61, 20);
            this.FileNameLabel.TabIndex = 12;
            this.FileNameLabel.Text = "LogFile";
            // 
            // textBoxLogFileName
            // 
            this.textBoxLogFileName.Location = new System.Drawing.Point(80, 213);
            this.textBoxLogFileName.Name = "textBoxLogFileName";
            this.textBoxLogFileName.Size = new System.Drawing.Size(733, 26);
            this.textBoxLogFileName.TabIndex = 13;
            // 
            // checkBoxMouseEvents
            // 
            this.checkBoxMouseEvents.AutoSize = true;
            this.checkBoxMouseEvents.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxMouseEvents.Location = new System.Drawing.Point(436, 25);
            this.checkBoxMouseEvents.Name = "checkBoxMouseEvents";
            this.checkBoxMouseEvents.Size = new System.Drawing.Size(227, 29);
            this.checkBoxMouseEvents.TabIndex = 14;
            this.checkBoxMouseEvents.Text = "Record mouse events";
            this.checkBoxMouseEvents.UseVisualStyleBackColor = true;
            // 
            // checkBoxKeyEvents
            // 
            this.checkBoxKeyEvents.AutoSize = true;
            this.checkBoxKeyEvents.Font = new System.Drawing.Font("Microsoft Sans Serif", 10F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.checkBoxKeyEvents.Location = new System.Drawing.Point(16, 25);
            this.checkBoxKeyEvents.Name = "checkBoxKeyEvents";
            this.checkBoxKeyEvents.Size = new System.Drawing.Size(249, 29);
            this.checkBoxKeyEvents.TabIndex = 15;
            this.checkBoxKeyEvents.Text = "Record keyboard events";
            this.checkBoxKeyEvents.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(825, 371);
            this.Controls.Add(this.checkBoxKeyEvents);
            this.Controls.Add(this.checkBoxMouseEvents);
            this.Controls.Add(this.textBoxLogFileName);
            this.Controls.Add(this.FileNameLabel);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.ActiveWinLabel);
            this.Controls.Add(this.KeyboardLayoutLabel);
            this.Controls.Add(this.KeyboardTypeLabel);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.checkBoxPlainText);
            this.Controls.Add(this.exitButton);
            this.Controls.Add(this.hideButton);
            this.Controls.Add(this.CheckBoxWinPlainText);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.Text = "TypingSpeedLogger";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.CheckBox CheckBoxWinPlainText;
        private System.Windows.Forms.Button hideButton;
        private System.Windows.Forms.Button exitButton;
        private System.Windows.Forms.CheckBox checkBoxPlainText;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label KeyboardTypeLabel;
        private System.Windows.Forms.Label KeyboardLayoutLabel;
        private System.Windows.Forms.Label ActiveWinLabel;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.NotifyIcon trayIcon;
        private System.Windows.Forms.Label FileNameLabel;
        private System.Windows.Forms.TextBox textBoxLogFileName;
        private System.Windows.Forms.CheckBox checkBoxMouseEvents;
        private System.Windows.Forms.CheckBox checkBoxKeyEvents;
    }
}

