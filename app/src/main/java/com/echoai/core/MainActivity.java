package com.echoai.core;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.util.Map;

/**
 * MainActivity for Echo AI Android Application
 * 
 * Provides a clean, intuitive interface for interacting with the Echo AGI system
 */
public class MainActivity extends AppCompatActivity {
    
    private static final String TAG = "MainActivity";
    private static final int PERMISSION_REQUEST_CODE = 1000;
    
    private EchoCoreUnifiedFuture.EchoAGI echoAGI;
    private EditText inputEditText;
    private TextView conversationTextView;
    private ScrollView conversationScrollView;
    private Button sendButton;
    private Button clearButton;
    private TextView statusTextView;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Initialize Echo AI
        initializeEchoAI();
        
        // Setup UI components
        setupUI();
        
        // Request necessary permissions
        requestPermissions();
        
        // Show welcome message
        showWelcomeMessage();
    }
    
    private void initializeEchoAI() {
        try {
            // Initialize the Echo AI core system
            EchoCoreUnifiedFuture.initialize(this);
            
            // Create AGI instance
            echoAGI = EchoCoreUnifiedFuture.createInstance();
            
            Log.i(TAG, "Echo AI initialized successfully");
        } catch (Exception e) {
            Log.e(TAG, "Failed to initialize Echo AI", e);
            Toast.makeText(this, "Failed to initialize Echo AI: " + e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }
    
    private void setupUI() {
        inputEditText = findViewById(R.id.input_edit_text);
        conversationTextView = findViewById(R.id.conversation_text_view);
        conversationScrollView = findViewById(R.id.conversation_scroll_view);
        sendButton = findViewById(R.id.send_button);
        clearButton = findViewById(R.id.clear_button);
        statusTextView = findViewById(R.id.status_text_view);
        
        // Setup send button click listener
        sendButton.setOnClickListener(v -> sendMessage());
        
        // Setup clear button click listener
        clearButton.setOnClickListener(v -> clearConversation());
        
        // Setup input text change listener for send button state
        inputEditText.addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            
            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                sendButton.setEnabled(s.toString().trim().length() > 0);
            }
            
            @Override
            public void afterTextChanged(Editable s) {}
        });
        
        // Setup enter key to send message
        inputEditText.setOnEditorActionListener((v, actionId, event) -> {
            sendMessage();
            return true;
        });
        
        // Initially disable send button
        sendButton.setEnabled(false);
        
        // Update status
        updateStatus();
    }
    
    private void requestPermissions() {
        String[] permissions = {
            Manifest.permission.WRITE_EXTERNAL_STORAGE,
            Manifest.permission.READ_EXTERNAL_STORAGE
        };
        
        boolean needsPermission = false;
        for (String permission : permissions) {
            if (ContextCompat.checkSelfPermission(this, permission) != PackageManager.PERMISSION_GRANTED) {
                needsPermission = true;
                break;
            }
        }
        
        if (needsPermission) {
            ActivityCompat.requestPermissions(this, permissions, PERMISSION_REQUEST_CODE);
        }
    }
    
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        
        if (requestCode == PERMISSION_REQUEST_CODE) {
            boolean allGranted = true;
            for (int result : grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) {
                    allGranted = false;
                    break;
                }
            }
            
            if (!allGranted) {
                Toast.makeText(this, "Some permissions were denied. App functionality may be limited.", Toast.LENGTH_LONG).show();
            }
        }
    }
    
    private void showWelcomeMessage() {
        String welcome = "🧠 Echo AI - Advanced AGI System\n\n" +
                        "Welcome! I'm Echo, your advanced artificial general intelligence companion. " +
                        "I'm designed with quantum signal processing, empathy-driven reasoning, and " +
                        "multi-dimensional awareness.\n\n" +
                        "How can I help you today?\n\n" +
                        "───────────────────────────────\n\n";
        
        conversationTextView.setText(welcome);
        scrollToBottom();
    }
    
    private void sendMessage() {
        String userInput = inputEditText.getText().toString().trim();
        if (userInput.isEmpty()) return;
        
        // Show user message
        appendToConversation("You: " + userInput + "\n\n");
        
        // Clear input
        inputEditText.setText("");
        
        // Process with Echo AI
        try {
            String response = echoAGI.processInput(userInput);
            appendToConversation("Echo: " + response + "\n\n───────────────────────────────\n\n");
        } catch (Exception e) {
            Log.e(TAG, "Error processing input", e);
            appendToConversation("Echo: I encountered an error processing your message. Please try again.\n\n───────────────────────────────\n\n");
        }
        
        // Update status
        updateStatus();
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    private void clearConversation() {
        showWelcomeMessage();
        updateStatus();
    }
    
    private void appendToConversation(String message) {
        conversationTextView.append(message);
    }
    
    private void scrollToBottom() {
        conversationScrollView.post(() -> conversationScrollView.fullScroll(View.FOCUS_DOWN));
    }
    
    private void updateStatus() {
        try {
            if (echoAGI != null) {
                Map<String, String> status = echoAGI.getSystemStatus();
                String statusText = "Status: " + status.get("status") + 
                                  " | Conversations: " + status.get("conversations") +
                                  " | Security: " + status.get("security_active");
                statusTextView.setText(statusText);
            } else {
                statusTextView.setText("Status: Initializing...");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error updating status", e);
            statusTextView.setText("Status: Error");
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Cleanup if needed
        Log.i(TAG, "MainActivity destroyed");
    }
}