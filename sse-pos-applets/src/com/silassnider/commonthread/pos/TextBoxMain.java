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
					commit();
				}
			}

		});
		add(input);
	}

	public void show_error() {
		this.input.setBackground(Color.RED);
	}

	public void add_chars(String new_char) {
		input.setText(input.getText() + new_char);
	}
	
	public String get_text(){
		return input.getText();
	}
	public void set_text(String text){
		input.setText(text);
	}
	public void commit(){
		JSObject interfac = JSObject.getWindow(me);
		interfac.call("process_input", new String[]{input.getText()});
		input.setText("");
	}
}
