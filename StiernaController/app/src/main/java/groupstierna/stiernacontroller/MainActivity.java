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

    private boolean connectionStatus = false;

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

        if (!StiernaConnector.send(mode.getMessage())) {
            updateConnectionStatus(false);
        }
        return true;
    }

    private void updateConnection() {
        StiernaConnector.setHostName(editTextIPNumber.getText().toString());
        StiernaConnector.setPortNumber(Integer.valueOf(editTextPortNumber.getText().toString()));
        updateConnectionStatus(StiernaConnector.updateConnection());
    }

    private void updateConnectionStatus(boolean status) {
        connectionStatus = status;
        if (connectionStatus) {
            textViewConnectionStatus.setText(R.string.connected);
        } else {
            textViewConnectionStatus.setText(R.string.disconnected);
        }
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
        if (mode.getMessage().matches(Keyword.MANUAL.getMessage())) {
            speed = Integer.toString(seekBarManualSpeed.getProgress());
        } else {
            speed = Integer.toString(seekBarACCSpeed.getProgress() - 100);
        }
        if (!StiernaConnector.send(Keyword.DRIVE.getMessage() + " " + speed)) {
            updateConnectionStatus(false);
        }
    }

    private void updateSteering() {
        String steering = Integer.toString(seekBarSteering.getProgress() - 100);
        if (!StiernaConnector.send(Keyword.STEER.getMessage() + " " + steering)) {
            updateConnectionStatus(false);
        }
    }
}
