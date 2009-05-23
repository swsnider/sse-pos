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
	public void init(){
		setBackground(Color.white);
		input = new JTextField();
		input.setColumns(20);
		input.addKeyListener(new KeyListener(){

			@Override
			public void keyPressed(KeyEvent arg0) {
				// TODO Auto-generated method stub
				
			}

			@Override
			public void keyReleased(KeyEvent arg0) {
				if (arg0.getKeyCode() == KeyEvent.VK_ENTER){
					interfaceObj.eval("process_input('" + input.getText() + "');");
					input.setText("");
				}
			}

			@Override
			public void keyTyped(KeyEvent arg0) {
			}
			
		});
		add(input);
	}
	
	public void init_js(JSObject obj){
		this.interfaceObj = obj;
	}
}
