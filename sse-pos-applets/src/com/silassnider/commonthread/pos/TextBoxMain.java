/**
 * 
 */
package com.silassnider.commonthread.pos;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.JApplet;
import javax.swing.JTextField;

import netscape.javascript.JSObject;

/**
 * @author Silas Snider
 * 
 */
public class TextBoxMain extends JApplet {
	JTextField input;
	JSObject interfaceObj;
    TextBoxMain me;

	public void init() {
		me = this;
		setBackground(Color.white);
		input = new JTextField();
		input.setColumns(20);
		input.addKeyListener(new KeyListener() {

			public void keyTyped(KeyEvent arg0) {
			}

			public void keyPressed(KeyEvent e) {
				// TODO Auto-generated method stub

			}

			public void keyReleased(KeyEvent e) {
				if (input.getBackground() == Color.RED)
					input.setBackground(Color.WHITE);
				if (e.getKeyCode() == KeyEvent.VK_ENTER) {
					JSObject interfac = JSObject.getWindow(me);
					interfac.call("process_input", new String[]{input.getText()});
					/*interfaceObj.eval("alert('" + input.getText()
							+ "');");
					interfaceObj.eval("process_input('" + input.getText()
							+ "');");*/
					input.setText("");
				}
				//input.setText("" + KeyEvent.VK_ENTER + "|" + e.getKeyCode());
			}

		});
		add(input);
	}

	public void init_js(JSObject obj) {
		this.interfaceObj = obj;
	}

	public void show_error() {
		this.input.setBackground(Color.RED);
	}

	public void add_chars(String new_char) {
		input.setText(input.getText() + new_char);
	}
}
