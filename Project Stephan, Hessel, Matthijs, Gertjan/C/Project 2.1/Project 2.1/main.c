#define F_CPU 16000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <stdbool.h>

#define UBBRVAL 51

double reading;
bool status = true; // true = ingeklapt // false = uitgeklapt
int stand = 0;
int max = 5; // 20 degree angle
int min = 0;

void transmit(char c) {
	loop_until_bit_is_set(UCSR0A, UDRE0); // wait until data register empty
	UDR0 = c;
}

uint16_t adc_read(uint8_t pin) {
	ADMUX	&=	0xf0;
	ADMUX	|=	pin;
	ADCSRA |= _BV(ADSC);
	while((ADCSRA & _BV(ADSC)));
	return ADC;
}

void getDistance(void) {
	PORTB &= ~_BV (1);
	_delay_us(2);
	PORTB |= _BV (1);
	_delay_us(10);
	PORTB &= ~_BV (1);
	loop_until_bit_is_set(PINB,2);
	TCNT1 = 0;
	loop_until_bit_is_clear(PINB,2);
	float count = ((float)TCNT1/16)/58*64*4;
	uint8_t distance = round(count);
	transmit(distance);
}

void getTemperature(void) {
	reading = adc_read(0);
	float voltage = reading * 5;
	voltage /= 1024;
	float tempC = (voltage - 0.5) * 100;
	uint8_t temp = round(tempC);
	transmit(temp);
}

void getLight(void) {
	reading = adc_read(1);
	reading = 1023 - reading;
	reading = reading * 255 / 1023;
	uint8_t light = round(reading);
	transmit(light);
}

uint8_t receive(void) {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}

void red_on(void) {
	PORTD |= _BV(PORTD5);

}
void red_off(void) {
	PORTD &= ~_BV(PORTD5);
}

void green_on(void) {
	PORTD |= _BV(PORTD7);
}

void green_off(void) {
	PORTD &= ~_BV(PORTD7);
}

void uitrol(void) {
	if (status == false) {
		transmit(77); // in- uitrol error
	}
	else {
		red_on();
		while(stand<max) {
			green_off();
			PORTD |= _BV(PORTD6);
			_delay_ms(400);
			PORTD &= ~_BV(PORTD6);
			_delay_ms(400);
			stand = stand + 1;
		}
		green_off();
		transmit(88);
		status = false;
	}
}

void inrol(void) {
	if (status == true) {
		transmit(77); //in- uitrol error
	}
	else {
		green_on();
		while(stand>min) {
			red_off();
			PORTD |= _BV(PORTD6);
			_delay_ms(400);
			PORTD &= ~_BV(PORTD6);
			_delay_ms(400);
			stand = stand - 1;
		}
		red_off();
		transmit(89);
		status = true;
	}
}

void protocol(void) {
	uint8_t task = receive();
	
	if(task == 53){
		inrol();
	}
	
	if(task == 54){
		uitrol();
	}
	
	if(task == 55) {
		getLight();
	}
	
	if(task == 56) {
		getTemperature();
	}
	
	if(task == 57) {
		getDistance();
	}

	if(task != 53 && task != 54 && task != 55 && task != 56 && task != 57) {
		transmit(69);
	}
}

void port_init(void) {
	DDRB |= _BV(1); // Trigger port
	DDRB &= ~_BV (2); // Echo port
	DDRD |= _BV(DDD7); // Green led
	DDRD |= _BV(DDD6); // Orange led
	DDRD |= _BV(DDD5); // Red led
	
	green_on();
	red_off();
}

int main(void) {
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	UCSR0A = 0;
	UCSR0B = _BV(TXEN0) | _BV(RXEN0);
	UCSR0C = _BV(UCSZ01) | _BV(UCSZ00);
	TCCR1B |= _BV(CS12);
	ADMUX = (1<<REFS0);
	ADCSRA = (1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);
	
	port_init();
	
	while(1) {
		protocol();
		_delay_ms(50);
	}
}