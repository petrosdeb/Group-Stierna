package groupstierna.stiernacontroller;

import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.MenuItem;
import android.view.View;
import android.widget.*;

public class MainActivity extends AppCompatActivity {

    private static final long COOLDOWN = 5;
    private TextView mTextMessage;
    private Keyword mode = Keyword.MANUAL;
    private RadioGroup radioGroup;
    private SeekBar seekBarSteering;
    private SeekBar seekBarManualSpeed;
    private SeekBar seekBarACCSpeed;
    private Button buttonUpdateConnection;
    private EditText editTextIPNumber;
    private EditText editTextPortNumber;
    private TextView textViewConnectionStatus;
    private TextView textViewSteeringDisplay;
    private TextView textViewManualSpeedDisplay;
    private TextView textViewACCSpeedDisplay;

    private String hostName = "192.168.0.0";
    private int portNumber = 9000;

    private Handler connectionStatusHandler;

    private boolean isConnected = false;

    private BottomNavigationView.OnNavigationItemSelectedListener mOnNavigationItemSelectedListener
            = new BottomNavigationView.OnNavigationItemSelectedListener() {

        @Override
        public boolean onNavigationItemSelected(@NonNull MenuItem item) {
            return updateMode();
        }

    };

    private RadioGroup.OnCheckedChangeListener radioGroupChangeListener = new RadioGroup.OnCheckedChangeListener() {
        @Override
        public void onCheckedChanged(RadioGroup group, int checkedId) {
            switch (checkedId) {
                case R.id.manualMode:
                    mode = Keyword.MANUAL;
                    break;
                case R.id.accMode:
                    mode = Keyword.ACC;
                    break;
                case R.id.platooningMode:
                    mode = Keyword.PLATOONING;
                    break;
            }
            updateMode();
        }
    };

    private Button.OnClickListener updateConnectionOnClickListener = new Button.OnClickListener() {
        @Override
        public void onClick(View v) {
            updateConnection();
        }
    };

    private SeekBar.OnSeekBarChangeListener manualSeekBarChangeListener = new SeekBar.OnSeekBarChangeListener() {
        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            updateControl();
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {

        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {
            seekBar.setProgress(100);
        }
    };

    private SeekBar.OnSeekBarChangeListener accSeekBarChangeListener = new SeekBar.OnSeekBarChangeListener() {
        @Override
        public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
            updateControl();
        }

        @Override
        public void onStartTrackingTouch(SeekBar seekBar) {

        }

        @Override
        public void onStopTrackingTouch(SeekBar seekBar) {

        }
    };

    private class ConnectionStatusTextWatcher implements TextWatcher{

        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {

        }

        @Override
        public void afterTextChanged(Editable s) {
            updateControlUsability();
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Buttons and stuff
        radioGroup = (RadioGroup) findViewById(R.id.radioGroup);
        seekBarSteering = (SeekBar) findViewById(R.id.seekBarSteering);
        seekBarManualSpeed = (SeekBar) findViewById(R.id.seekBarManualSpeed);
        seekBarACCSpeed = (SeekBar) findViewById(R.id.seekBarACCSpeed);
        buttonUpdateConnection = (Button) findViewById(R.id.buttonUpdateConnection);

        // Text stuff
        editTextIPNumber = (EditText) findViewById(R.id.textIPNumber);
        editTextPortNumber = (EditText) findViewById(R.id.textPortNumber);
        textViewConnectionStatus = (TextView) findViewById(R.id.textViewConnectionStatus);
        textViewSteeringDisplay = (TextView) findViewById(R.id.textViewSteeringDisplay);
        textViewManualSpeedDisplay = (TextView) findViewById(R.id.textViewManualSpeedDisplay);
        textViewACCSpeedDisplay = (TextView) findViewById(R.id.textViewACCSpeedDisplay);
        textViewConnectionStatus.setText(R.string.disconnected);

        setSeekBarDefaultValues();

        // Listeners
        radioGroup.setOnCheckedChangeListener(radioGroupChangeListener);
        seekBarSteering.setOnSeekBarChangeListener(manualSeekBarChangeListener);
        seekBarManualSpeed.setOnSeekBarChangeListener(manualSeekBarChangeListener);
        seekBarACCSpeed.setOnSeekBarChangeListener(accSeekBarChangeListener);
        buttonUpdateConnection.setOnClickListener(updateConnectionOnClickListener);

        textViewConnectionStatus.addTextChangedListener(new ConnectionStatusTextWatcher());

        connectionStatusHandler = new Handler(Looper.getMainLooper()){
            @Override
            public void handleMessage(Message inputMessage){
                isConnected = (Boolean) inputMessage.obj;
                textViewConnectionStatus.setText(inputMessage.arg1);
            }
        };

        updateControlUsability();
    }

    private void setSeekBarDefaultValues() {
        seekBarACCSpeed.setProgress(50);
        seekBarManualSpeed.setProgress(100);
        seekBarSteering.setProgress(100);
    }

    private enum Keyword {
        MANUAL("m"), ACC("a"), PLATOONING("p"), DRIVE("d"), STEER("s");
        private final String message;

        Keyword(String message) {
            this.message = message;
        }

        public String getMessage() {
            return message;
        }
    }

    private boolean updateMode() {
        switch (radioGroup.getCheckedRadioButtonId()) {
            case R.id.manualMode:
                mode = Keyword.MANUAL;
                break;
            case R.id.accMode:
                mode = Keyword.ACC;
                break;
            case R.id.platooningMode:
                mode = Keyword.PLATOONING;
                break;
            default:
                return false;
        }

        if (mode == Keyword.MANUAL) {
            trySend(mode.getMessage());
        } else {
            updateSpeed();
        }
        return true;
    }

    private void updateConnection() {
        hostName = editTextIPNumber.getText().toString();
        portNumber = Integer.valueOf(editTextPortNumber.getText().toString());
        updateConnectionStatus();
    }

    private void updateConnectionStatus() {
        trySend("");
    }

    private void updateControlUsability() {
        if (isConnected) {
            switch (mode) {
                case MANUAL:
                    seekBarSteering.setEnabled(true);
                    seekBarManualSpeed.setEnabled(true);
                    seekBarACCSpeed.setEnabled(true);
                    break;
                case ACC:
                    seekBarSteering.setEnabled(true);
                    seekBarManualSpeed.setEnabled(false);
                    seekBarACCSpeed.setEnabled(true);
                    break;
                case PLATOONING:
                    seekBarSteering.setEnabled(false);
                    seekBarManualSpeed.setEnabled(false);
                    seekBarACCSpeed.setEnabled(true);
                    break;
            }
        } else {
            seekBarSteering.setEnabled(false);
            seekBarManualSpeed.setEnabled(false);
            seekBarACCSpeed.setEnabled(false);
        }
        seekBarSteering.invalidate();
        seekBarManualSpeed.invalidate();
        seekBarACCSpeed.invalidate();
    }

    public void updateControl() {
        updateSpeed();
        if(mode != Keyword.PLATOONING) {
            updateSteering();
        }
        textViewSteeringDisplay.setText(String.valueOf(seekBarSteering.getProgress() - 100));
        textViewManualSpeedDisplay.setText(String.valueOf(seekBarManualSpeed.getProgress() - 100));
        textViewACCSpeedDisplay.setText(String.valueOf(seekBarACCSpeed.getProgress()));
    }

    private void updateSpeed() {
        if (mode == Keyword.MANUAL) {
            trySend(Keyword.DRIVE.getMessage() + " " + Integer.toString(seekBarManualSpeed.getProgress() - 100));
        } else {
            trySend(mode.getMessage() + " " + Integer.toString(seekBarACCSpeed.getProgress()));
        }
    }

    private void updateSteering() {
        trySend(Keyword.STEER.getMessage() + " " + Integer.toString(seekBarSteering.getProgress() - 100));
    }

    private void trySend(String message) {
        StiernaAsyncClient client = new StiernaAsyncClient(hostName, portNumber, message, connectionStatusHandler);
        client.execute();
    }
}
