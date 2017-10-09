package groupstierna.stiernacontroller;

import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.design.widget.BottomNavigationView;
import android.support.v7.app.AppCompatActivity;
import android.view.MenuItem;
import android.view.View;
import android.widget.*;

public class MainActivity extends AppCompatActivity {

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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        radioGroup = (RadioGroup) findViewById(R.id.radioGroup);
        seekBarSteering = (SeekBar) findViewById(R.id.seekBarSteering);
        seekBarManualSpeed = (SeekBar) findViewById(R.id.seekBarManualSpeed);
        seekBarACCSpeed = (SeekBar) findViewById(R.id.seekBarACCSpeed);
        buttonUpdateConnection = (Button) findViewById(R.id.buttonUpdateConnection);

        editTextIPNumber = (EditText) findViewById(R.id.textIPNumber);
        editTextPortNumber = (EditText) findViewById(R.id.textPortNumber);
        textViewConnectionStatus = (TextView) findViewById(R.id.textViewConnectionStatus);
        textViewSteeringDisplay = (TextView) findViewById(R.id.textViewSteeringDisplay);
        textViewManualSpeedDisplay = (TextView) findViewById(R.id.textViewManualSpeedDisplay);
        textViewACCSpeedDisplay = (TextView) findViewById(R.id.textViewACCSpeedDisplay);

        setSeekBarDefaultValues();

        radioGroup.setOnCheckedChangeListener(radioGroupChangeListener);
        seekBarSteering.setOnSeekBarChangeListener(manualSeekBarChangeListener);
        seekBarManualSpeed.setOnSeekBarChangeListener(manualSeekBarChangeListener);
        seekBarACCSpeed.setOnSeekBarChangeListener(accSeekBarChangeListener);
        buttonUpdateConnection.setOnClickListener(updateConnectionOnClickListener);

        textViewConnectionStatus.setText(R.string.disconnected);
        updateControlUsability();
    }

    private void setSeekBarDefaultValues() {
        seekBarACCSpeed.setProgress(50);
        seekBarManualSpeed.setProgress(100);
        seekBarSteering.setProgress(100);
    }

    private static enum Keyword {
        MANUAL("m"), ACC("a"), PLATOONING("p"), DRIVE("d"), STEER("s");
        private final String message;

        private Keyword(String message) {
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

        trySend(mode.getMessage());
        if (mode == Keyword.ACC) {
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
        if (textViewConnectionStatus.getText() == "Connected") {
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
        updateSteering();
        textViewSteeringDisplay.setText(String.valueOf(seekBarSteering.getProgress() - 100));
        textViewManualSpeedDisplay.setText(String.valueOf(seekBarManualSpeed.getProgress() - 100));
        textViewACCSpeedDisplay.setText(String.valueOf(seekBarACCSpeed.getProgress()));
    }

    private void updateSpeed() {
        String speed = "";
        if (mode == Keyword.MANUAL) {
            speed = Integer.toString(seekBarManualSpeed.getProgress() - 100);
        } else {
            speed = Integer.toString(seekBarACCSpeed.getProgress());
        }
        trySend(Keyword.DRIVE.getMessage() + " " + speed);
    }

    private void updateSteering() {
        String steering = Integer.toString(seekBarSteering.getProgress() - 100);
        trySend(Keyword.STEER.getMessage() + " " + steering);
    }

    private void trySend(String message) {
        StiernaAsyncClient client = new StiernaAsyncClient(hostName, portNumber, message, textViewConnectionStatus);
        client.execute();
        updateControlUsability();
    }
}
