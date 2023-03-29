import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

export default function App() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [cycleLength, setCycleLength] = useState('');

  const handleSave = () => {
    fetch('http://localhost:5000/periods', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        start_date: startDate,
        end_date: endDate,
        cycle_length: cycleLength
      })
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
  };

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Period Tracker</Text>
      <TextInput
        style={styles.input}
        placeholder="Start Date"
        onChangeText={text => setStartDate(text)}
        value={startDate}
      />
      <TextInput
        style={styles.input}
        placeholder="End Date"
        onChangeText={text => setEndDate(text)}
        value={endDate}
      />
      <TextInput
        style={styles.input}
        placeholder="Cycle Length"
        keyboardType="numeric"
        onChangeText={text => setCycleLength(text)}
        value={cycleLength}
      />
      <Button title="Save" onPress={handleSave} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    margin: 10,
    width: '80%',
    borderRadius: 5,
  },
});